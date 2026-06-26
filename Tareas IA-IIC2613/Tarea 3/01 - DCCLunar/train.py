import gymnasium as gym
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from LunarLanderAgent import LunarLanderAgent

# Parámetros de entrenamiento
NUM_EPISODES = 100000
PRINT_EVERY = 100
RESULTS_DIR = "results"
LC_CSV  = os.path.join(RESULTS_DIR, "learning_curve.csv")

def train(save_npy_path, save_csv_path, save_png_path, experiment_name='final'): # Usé esto para la act 3
    # Entrena un agente Q-Learning para LunarLander y guarda los resultados
    env = make_env()
    agent = LunarLanderAgent(env)

    # Esto nos sirve para identificar los hiperparams (experimento)
    hparams = {
        "learning_rate":    agent.learning_rate,
        "discount_factor":  agent.discount_factor,
        "epsilon_decay":    agent.epsilon_decay_rate,
        "min_epsilon":      agent.min_epsilon,
    }
    print(f"\n{'='*60}")
    print(f"Experimento : {experiment_name}")
    print(f"Hiperparáms : {hparams}")
    print(f"{'='*60}\n")

    mean_scores = []
    block_rewards = []
    lc_rows = []
    best_block_mean = -np.inf

    for episode in range(1, NUM_EPISODES + 1):
        observation, _ = env.reset()
        state = agent.get_state(observation)
        terminated = False
        truncated = False
        episode_reward = 0.0

        while not (terminated or truncated):
            action = agent.get_action(state, training=True)
            next_observation, reward, terminated, truncated, _ = env.step(action)
            next_state = agent.get_state(next_observation)

            done = terminated or truncated
            agent.update_q_value(state, action, reward, next_state, done)

            state = next_state
            episode_reward += reward

        agent.n_games += 1
        agent.decay_exploration_rate()
        block_rewards.append(episode_reward)

        if episode % PRINT_EVERY == 0:
            recent_rewards = np.array(block_rewards[-PRINT_EVERY:], dtype=np.float32)
            block_mean = float(np.mean(recent_rewards))
            block_record = float(np.max(recent_rewards))
            pct_negative = float(np.mean(recent_rewards < 0.0) * 100.0)
            pct_solutions = float(np.mean(recent_rewards > 200.0) * 100.0)

            mean_scores.append(block_mean)
            best_block_mean = max(best_block_mean, block_mean)

            # Tomamos una fila por bloque 
            lc_rows.append({
                "experiment":       experiment_name,
                "learning_rate":    hparams["learning_rate"],
                "discount_factor":  hparams["discount_factor"],
                "episode":          episode,
                "block_mean_score": block_mean,
                "block_record":     block_record,
                "pct_negative":     pct_negative,
                "pct_solutions":    pct_solutions,
                "epsilon":          agent.exploration_rate,
            })

            print(
                f"Episode {episode:6d} | mean score: {block_mean:8.2f} | "
                f"record: {block_record:8.2f} | % reward < 0: {pct_negative:6.2f}% | "
                f"% solutions: {pct_solutions:5.1f}% | epsilon: {agent.exploration_rate:6.4f}"
            )

    np.save(save_npy_path, agent.q_table)
    agent.export_q_table_csv(save_csv_path)
    plot_learning_curve(block_record, save_png_path)

    _append_csv(lc_rows, LC_CSV)

    env.close()
    print(f"\nExperimento '{experiment_name}', guardado en {LC_CSV}")
    
    return agent

# Uso de IA [1]
def _append_csv(rows, path):
    os.makedirs(RESULTS_DIR, exist_ok=True)
    df = pd.DataFrame(rows)
    if os.path.exists(path):
        df.to_csv(path, mode="a", header=False, index=False)
    else:
        df.to_csv(path, index=False)

def make_env():
    # Crea el entorno de LunarLander con parámetros fijos
    env = gym.make("LunarLander-v3", continuous=False, gravity=-10.0, enable_wind=False,
                   wind_power=15.0, turbulence_power=1.5)
    return gym.wrappers.RecordEpisodeStatistics(env, buffer_length=NUM_EPISODES)

def plot_learning_curve(block_record, output_path):
    # Grafica la curva de aprendizaje y la guarda como imagen
    plt.figure(figsize=(10, 5))
    plt.plot(block_record)
    plt.xlabel(f"Bloques de {PRINT_EVERY} episodios")
    plt.ylabel("Record")
    plt.title("Aprendizaje de LunarLander con Q-Learning")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def plot_td_error(mean_tds, output_path):
    # Muestra como el error entre lo que se predice y lo que se obtiene 
    # cambia con el paso de iteraciones
    plt.figure(figsize=(10, 5))
    plt.plot(mean_tds)
    plt.xlabel(f"Bloques de 10000 pasos")
    plt.ylabel("Mean TD Error")
    plt.title("Error de predicción TD")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()