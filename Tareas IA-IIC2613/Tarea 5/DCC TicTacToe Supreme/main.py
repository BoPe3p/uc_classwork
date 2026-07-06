import pygame
from player import HumanPlayer, MinimaxPlayer
from ui import UI
from score import evaluate, strategic_eval, custom_eval
from ResultCollection import ResultCollection

N = 10

def main():
    # Cambia aqui la combinacion de jugadores:
    #player1 = HumanPlayer("Player 1")
    #player2 = HumanPlayer("Player 2")

    # player1 = HumanPlayer("Player 1")
    # player2 = MinimaxPlayer("AI", depth=2, eval_fun=evaluate, use_alphabeta=True)

    # Experimentos IA vs IA
    for _ in range(N):
        player1 = MinimaxPlayer("AI 1", depth=3, eval_fun=custom_eval, use_alphabeta=True)
        player2 = MinimaxPlayer("AI 2", depth=3, eval_fun=strategic_eval, use_alphabeta=True)

    # headless = False si se muestra la UI siempre
    # headless = True oculta la UI solo si ambos jugadores son AI
        ui = UI(player1, player2, headless=True)
        ui.run()

        results = ResultCollection.get_results()
        # USO DE IA
        print("\n% Tabla LaTeX")
        print(r'\begin{table}[htbp]')
        print(r'\centering')
        print(r"\begin{tabular}{cllllccrr}")
        print(r"\hline")
        print(r"Juego & Ganador & Eval P1 & Eval P2 & D1 & D2 & Avg T P1 & Avg T P2 \\")
        print(r"\hline")
        for i, r in enumerate(results, 1):
            print(f"{i} & {r['WINNER']} & {r['EVALUATION_FUNCTION_PLAYER_1']} & {r['EVALUATION_FUNCTION_PLAYER_2']} & {r['DEPTH_PLAYER_1']} & {r['DEPTH_PLAYER_2']} & {r['AVG_TIME_PLAYER_1']:.3f}s & {r['AVG_TIME_PLAYER_2']:.3f}s \\\\")
        print(r"\hline")
        print(r"\end{tabular}")
        print(r"\end{table}")


if __name__ == "__main__":
    main()
