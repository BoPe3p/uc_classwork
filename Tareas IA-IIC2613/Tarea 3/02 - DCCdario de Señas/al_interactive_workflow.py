import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from IPython.display import HTML, display
from sklearn.base import clone
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from skactiveml.classifier import SklearnClassifier
from skactiveml.pool import UncertaintySampling
from IPython.display import display, HTML, clear_output
import sys
import time


class Viewer:
    """Encapsula historial, eventos y renderizado de Active Learning."""

    def __init__(self, image_base_dir=None, image_index=None):
        self.image_base_dir = image_base_dir
        self.image_index = image_index
        self._rows = []
        self._event_rows = []
        self._label_logs = []
        self._render_progress_plot_handle = None
        self._render_progress_table_handle = None
        self._render_labeling_events_table_handle = None

    def reiniciar(self):
        self._rows.clear()
        self._event_rows.clear()
        self._label_logs.clear()
        self._reset_progress_handles()

    def agregar_historial(self, iteration, etiquetadas, accuracy, precision_macro, recall_macro, class_counts=None):
        if class_counts is None:
            class_counts = {}

        previous_counts = {}
        if self._rows:
            last_row = self._rows[-1]
            previous_counts = {
                str(col)[len("label_count_") :]: int(last_row[col])
                for col in last_row.keys()
                if str(col).startswith("label_count_")
            }

        cumulative_counts = dict(previous_counts)
        for cls, count in class_counts.items():
            cumulative_counts[str(cls)] = cumulative_counts.get(str(cls), 0) + int(count)

        class_counts_render = {f"label_count_{cls}": count for cls, count in cumulative_counts.items()}

        row = {
            "iteracion": int(iteration),
            "etiquetadas": int(etiquetadas),
            "accuracy": float(accuracy),
            "precision_macro": float(precision_macro),
            "recall_macro": float(recall_macro),
            **class_counts_render,
        }
        self._rows.append(row)

        print(
            f"Iteracion {row['iteracion']} | "
            f"etiquetadas={row['etiquetadas']} | "
            f"acc={row['accuracy']:.4f} | "
            f"precision={row['precision_macro']:.4f} | "
            f"recall={row['recall_macro']:.4f}"
        )

        self._render_progress(self.obtener_historial_df())

    def obtener_historial_df(self):
        return pd.DataFrame(self._rows)

    def actualizar_tabla_eventos(self):
        self._render_labeling_events(self._event_rows)

    def solicitar_etiquetado(self, indices, class_names, filenames, iteration=1):
        answers, logs = self._ask_label_for_indices(indices=indices, class_names=class_names, filenames=filenames, iteration=iteration)
        self._label_logs.extend(logs)
        self.actualizar_tabla_eventos()
        return answers

    @staticmethod
    def _update_display_handle(handle, content):
        if handle is None:
            return display(content, display_id=True)
        handle.update(content)
        return handle

    @staticmethod
    def _ask_choice(title, options):
        print(f"\n{title}")
        for i, opt in enumerate(options, start=1):
            print(f"  {i}. {opt}")
        
        sys.stdout.flush()
        time.sleep(0.1)

        while True:
            raw = input("Elige una opcion (numero o texto exacto): ").strip()
            if raw in options:
                return raw
            if raw.isdigit():
                idx = int(raw) - 1
                if 0 <= idx < len(options):
                    return options[idx]
            print("Entrada invalida. Intenta nuevamente.")

    @staticmethod
    def _build_image_index(image_base_dir):
        image_index = {}
        if image_base_dir is None or not os.path.isdir(image_base_dir):
            return image_index

        for root, _, files in os.walk(image_base_dir):
            for fname in files:
                key = str(fname).strip().lower()
                if key not in image_index:
                    image_index[key] = []
                image_index[key].append(os.path.join(root, fname))

        return image_index

    def _resolve_image_path(self, filename, class_names,label_hint=None):
        filename = str(filename).strip()
        if filename == "" or filename.lower() == "nan":
            return None

        if os.path.isabs(filename) and os.path.exists(filename):
            return filename

        direct_path = os.path.join(self.image_base_dir, filename)
        if os.path.exists(direct_path):
            return direct_path

        if label_hint is not None:
            hinted = os.path.join(self.image_base_dir, str(label_hint), filename)
            if os.path.exists(hinted):
                return hinted

        if class_names is not None:
            for cls in class_names:
                candidate = os.path.join(self.image_base_dir, str(cls), filename)
                if os.path.exists(candidate):
                    return candidate

        matches = self.image_index.get(filename.lower(), [])
        if len(matches) == 1:
            return matches[0]
        if len(matches) > 1 and label_hint is not None:
            token = f"/{label_hint}/"
            for m in matches:
                if token in m.replace("\\", "/"):
                    return m
            return matches[0]

        return None

    def _show_image_temporarily(self, image_path, idx, filename):
        if image_path is None or not os.path.exists(image_path):
            return False, None

        img_bgr = cv2.imread(image_path)
        if img_bgr is None:
            return False, None

        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.imshow(img_rgb)
        ax.set_title(f"idx={idx} | archivo={filename}")
        ax.axis("off")
        fig.tight_layout()
        handle = display(fig, display_id=True)
        plt.close(fig)
        return True, handle

    def _clear_display_handle(self, handle):
        if handle is None:
            return
        try:
            handle.update(HTML(""))
        except Exception:
            pass

    def _render_progress(self, history_df):
        if history_df.empty:
            return

        fig, axes = plt.subplots(1, 3, figsize=(18, 4))

        axes[0].plot(history_df["iteracion"], history_df["accuracy"], marker="o", label="Accuracy")
        axes[0].plot(history_df["iteracion"], history_df["precision_macro"], marker="o", label="Precision")
        axes[0].plot(history_df["iteracion"], history_df["recall_macro"], marker="o", label="Recall")
        axes[0].set_title("Progreso del modelo")
        axes[0].set_xlabel("Iteracion")
        axes[0].set_ylabel("Score")
        axes[0].grid(alpha=0.3)
        axes[0].legend()

        acc0 = history_df["accuracy"].iloc[0]
        improvement = history_df["accuracy"] - acc0
        axes[1].plot(history_df["iteracion"], improvement, marker="o", color="green")
        axes[1].axhline(0.0, linestyle="--", linewidth=1, color="gray")
        axes[1].set_title("Mejora acumulada de Accuracy")
        axes[1].set_xlabel("Iteracion")
        axes[1].set_ylabel("Accuracy - Accuracy inicial")
        axes[1].grid(alpha=0.3)

        iterations = history_df["iteracion"].to_numpy(dtype=float)
        label_cols = [col for col in history_df.columns if str(col).startswith("label_count_")]
        class_names = [str(col)[len("label_count_"):] for col in label_cols]
        n_classes = len(class_names)
        bar_width = 0.8 / max(1, n_classes)

        for k, col in enumerate(label_cols):
            cls = str(col)[len("label_count_") :]
            offset = (k - (n_classes - 1) / 2) * bar_width
            axes[2].bar(iterations + offset, history_df[col], width=bar_width, label=str(cls), alpha=0.9)

        axes[2].set_title("Etiquetados por clase")
        axes[2].set_xlabel("Iteracion")
        axes[2].set_ylabel("Numero de etiquetados")
        axes[2].set_xticks(iterations)
        axes[2].grid(axis="y", alpha=0.3)
        if n_classes > 0:
            axes[2].legend(ncol=min(3, n_classes))

        fig.tight_layout()
        self._render_progress_plot_handle = self._update_display_handle(self._render_progress_plot_handle, fig)
        plt.close(fig)

        tail_html = history_df.to_html(index=False)
        self._render_progress_table_handle = self._update_display_handle(self._render_progress_table_handle, HTML(tail_html))

    def _render_labeling_events(self, event_rows, max_rows=15):
        columns = [
            "evento",
            "iteracion",
            "idx_pool",
            "filename",
            "image_path",
            "imagen_mostrada",
            "label_elegida",
        ]

        if len(event_rows) == 0:
            html = "<b>Actividad de etiquetado</b><br><i>Sin eventos todavia.</i>"
        else:
            df_events = pd.DataFrame(event_rows)
            for col in columns:
                if col not in df_events.columns:
                    df_events[col] = ""
            html = df_events[columns].to_html(index=False)

        self._render_labeling_events_table_handle = self._update_display_handle(
            self._render_labeling_events_table_handle,
            HTML(html),
        )

    def _reset_progress_handles(self):
        self._render_progress_plot_handle = None
        self._render_progress_table_handle = None
        self._render_labeling_events_table_handle = None

    def _ask_label_for_indices(self, indices, class_names, filenames, iteration=1):
        class_set = set(class_names)
        answers = {}
        logs = []

        filenames = np.asarray(filenames)
        event_rows = self._event_rows

        for idx in indices:
            filename = filenames[idx]
            image_path = self._resolve_image_path(filename=filename, class_names=class_names, label_hint=None)
            shown, image_handle = self._show_image_temporarily(image_path, idx, filename)

            row_idx = len(event_rows)
            event_rows.append(
                {
                    "evento": "mostrando",
                    "iteracion": int(iteration),
                    "idx_pool": int(idx),
                    "filename": None if filename is None else str(filename),
                    "image_path": None if image_path is None else str(image_path),
                    "imagen_mostrada": bool(shown),
                    "label_elegida": "",
                }
            )
            self._render_labeling_events(event_rows)

            while True:
                prompt = f"\nEtiqueta para idx={idx}, archivo={filename} (opciones: {', '.join(class_names)}): "
                
                print(prompt)
                sys.stdout.flush()
                time.sleep(0.1)
                label = input(">>> ").strip()
                
                if label in class_set:
                    answers[idx] = label
                    logs.append(
                        {
                            "iteracion": iteration,
                            "idx_pool": int(idx),
                            "filename": None if filename is None else str(filename),
                            "image_path": None if image_path is None else str(image_path),
                            "imagen_mostrada": bool(shown),
                            "label_elegida": label,
                        }
                    )
                    break
                print("Etiqueta invalida. Debe ser una de las opciones permitidas.")

            self._clear_display_handle(image_handle)

            event_rows[row_idx]["evento"] = "registrado"
            event_rows[row_idx]["label_elegida"] = str(answers[idx])
            self._render_labeling_events(event_rows)

        return answers, logs

