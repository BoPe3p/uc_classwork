import sys
import os
sys.path.append(os.path.dirname(__file__))

from train import train

# Esto se cambia para diferenciar experimentos
EXPERIMENT_NAME = "Agente_propuesto"

if __name__ == "__main__":
    os.makedirs("results", exist_ok=True)

    train(
    save_npy_path=f"results/{EXPERIMENT_NAME}_qtable.npy",
    save_csv_path=f"results/{EXPERIMENT_NAME}_qtable.csv",
    save_png_path=f"results/{EXPERIMENT_NAME}_lc.png",
    experiment_name=EXPERIMENT_NAME,
    )