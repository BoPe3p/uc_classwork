import pygame
from player import HumanPlayer, MinimaxPlayer
from ui import UI
from score import evaluate, strategic_eval
from ResultCollection import ResultCollection

N = 10

def main():
    for i in range(N):
        player1 = MinimaxPlayer("AI 1", depth=1, eval_fun=evaluate, use_alphabeta=True)
        player2 = MinimaxPlayer("AI 2", depth=1, eval_fun=evaluate, use_alphabeta=True)
        ui = UI(player1, player2, headless=True)
        ui.run()
    
    for r in ResultCollection.get_results():
        print(r)

if __name__ == "__experiments__":
    main()