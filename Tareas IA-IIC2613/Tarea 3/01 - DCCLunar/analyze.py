import pandas as pd
import matplotlib.pyplot as plt
import os

RESULTS_DIR = "results"
LC_CSV = os.path.join(RESULTS_DIR, "learning_curve.csv")

# Cambiar para los experimentos
EXPERIMENTS = ["Agente_ideal_exp", "Agente_propuesto"]

def get_data(csv_path):
    df = pd.read_csv(csv_path)
    return df[df["experiment"].isin(EXPERIMENTS)]  # filtramos los que nos interesan

def plot_learning_curve():
    df = get_data(LC_CSV)
    plt.figure(figsize=(12, 5))
    for exp in EXPERIMENTS:
        group = df[df["experiment"] == exp]
        plt.plot(group["episode"].values, group["block_mean_score"].values, label=exp)
    plt.xlabel("Episodio")
    plt.ylabel("Mean Score")
    plt.title("Comparación: Learning Curve")
    plt.legend()
    plt.tight_layout()
    path = os.path.join(RESULTS_DIR, "compare_learning_curve.png")
    plt.savefig(path)
    plt.show()
    print(f"Guardado: {path}")

# Uso IA [2]
def save_table_as_image(df, columns, filename):
    fig, ax = plt.subplots(figsize=(10, len(df) * 0.4 + 1))
    ax.axis("off")
    tabla = ax.table(
        cellText=df[columns].values,
        colLabels=columns,
        loc="center",
        cellLoc="center"
    )
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(9)
    tabla.auto_set_column_width(col=list(range(len(columns))))
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Tabla guardada: {filename}")

def print_tabla():
    df = get_data(LC_CSV)

    dfs = {}
    for exp in EXPERIMENTS:
        g = df[df["experiment"] == exp].copy()
        g = g[g["episode"] % 1000 == 0]  # filtrar cada 1000 episodios
        dfs[exp] = g[["episode", "block_mean_score", "block_record"]].copy()
        dfs[exp].columns = ["Episodio", f"Mean ({exp})", f"Record ({exp})"]

    # Uso de IA [3] Unir lado a lado por episodio
    tabla = dfs[EXPERIMENTS[0]]
    for exp in EXPERIMENTS[1:]:
        tabla = tabla.merge(dfs[exp], on="Episodio")

    for col in tabla.columns:
        if col != "Episodio":
            tabla[col] = tabla[col].round(2)
    print("\n── Tabla Comparativa ──")
    print(tabla.to_string(index=False))
    tabla.to_csv(os.path.join(RESULTS_DIR, "tabla_comparativa.csv"), index=False)
    save_table_as_image(tabla,
                        columns=tabla.columns.tolist(),
                        filename="results/tabla_comparativa.png")

def plot_epsilon():
    df = get_data(LC_CSV)
    plt.figure(figsize=(12, 5))
    for exp in EXPERIMENTS:
        group = df[df["experiment"] == exp]
        plt.plot(group["episode"].values, group["epsilon"].values, label=exp)
    plt.xlabel("Episodio")
    plt.ylabel("Epsilon")
    plt.title("Comparación: Epsilon Decay")
    plt.legend()
    plt.tight_layout()
    path = os.path.join(RESULTS_DIR, "compare_epsilon.png")
    plt.savefig(path)
    plt.show()
    print(f"Guardado: {path}")

plot_learning_curve()
#print_tabla()
plot_epsilon()