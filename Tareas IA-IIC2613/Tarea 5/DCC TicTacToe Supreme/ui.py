# NO TOCAR
import pygame
import sys
import time
from game import Game
from minimax import minimax
from board import (EMPTY, X, O, CELL_SIZE, MINI_GAP, META_GAP, MARGIN,
                   WHITE, BLACK, LIGHT, BLUE, RED, YELLOW, GREEN, GRAY)
from ResultCollection import ResultCollection

FPS = 30

pygame.init()
FONT = pygame.font.SysFont(None, 20)
FONT_MED = pygame.font.SysFont(None, 36)


def compute_window_size():
    mini_size = CELL_SIZE * 3 + MINI_GAP * 2
    board_size = mini_size * 3 + META_GAP * 2
    width = MARGIN * 2 + board_size
    height = width + 60
    return width, height


class UI:
    def __init__(self, player1, player2, headless=False):
        self.players = [player1, player2]
        self.headless = headless and (not player1.is_human) and (not player2.is_human)
        self.window_w, self.window_h = compute_window_size()

        if self.headless:
            self.screen = None
            self.clock = pygame.time.Clock()
        else:
            self.screen = pygame.display.set_mode((self.window_w, self.window_h))
            pygame.display.set_caption("DCC TicTacToe Supreme")
            self.clock = pygame.time.Clock()

        self.game = Game()
        self.running = True
        self.total_time = [0.0, 0.0]
        self.move_counts = [0, 0]

        if not self.players[self.game.turn % 2].is_human:
            if not self.headless:
                pygame.event.post(pygame.event.Event(pygame.USEREVENT + 1))

    def _mini_origin(self, br, bc):
        mini_size = CELL_SIZE * 3 + MINI_GAP * 2
        x = MARGIN + bc * (mini_size + META_GAP)
        y = MARGIN + br * (mini_size + META_GAP)
        return x, y

    def _cell_rect(self, br, bc, cr, cc):
        ox, oy = self._mini_origin(br, bc)
        x = ox + cc * (CELL_SIZE + MINI_GAP)
        y = oy + cr * (CELL_SIZE + MINI_GAP)
        return pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

    def pixel_to_move(self, mx, my):
        for br in range(3):
            for bc in range(3):
                for cr in range(3):
                    for cc in range(3):
                        rect = self._cell_rect(br, bc, cr, cc)
                        if rect.collidepoint(mx, my):
                            return br, bc, cr, cc
        return None

    def draw(self):
        if self.headless:
            return

        self.screen.fill(WHITE)
        ab = self.game.board.active_board

        for br in range(3):
            for bc in range(3):
                mini = self.game.board.get_mini(br, bc)
                ox, oy = self._mini_origin(br, bc)
                mini_w = CELL_SIZE * 3 + MINI_GAP * 2
                mini_h = mini_w

                is_active = (ab is None and not mini.is_done()) or (ab == (br, bc))
                if is_active:
                    pygame.draw.rect(self.screen, YELLOW, (ox - 3, oy - 3, mini_w + 6, mini_h + 6), 3)

                if mini.is_done() and mini.winner != EMPTY:
                    overlay = pygame.Surface((mini_w, mini_h), pygame.SRCALPHA)
                    color = (*BLUE, 60) if mini.winner == X else (*RED, 60)
                    overlay.fill(color)
                    self.screen.blit(overlay, (ox, oy))

                for cr in range(3):
                    for cc in range(3):
                        rect = self._cell_rect(br, bc, cr, cc)
                        pygame.draw.rect(self.screen, LIGHT, rect)
                        pygame.draw.rect(self.screen, GRAY, rect, 1)

                        cell = mini.cells[cr][cc]
                        if cell == X:
                            self._draw_x(rect)
                        elif cell == O:
                            self._draw_o(rect)

                if mini.is_done() and mini.winner != EMPTY:
                    self._draw_conquered_mark(
                        "X" if mini.winner == X else "O",
                        BLUE if mini.winner == X else RED,
                        pygame.Rect(ox, oy, mini_w, mini_h),
                    )

        current = self.players[self.game.turn % 2]
        mark = "X" if self.game.current_player() == X else "O"
        info = f"Turno: {current.name} ({mark})"
        self.screen.blit(FONT.render(info, True, BLACK), (10, self.window_h - 50))

        if self.game.winner is not None:
            winner_name = self.players[self.game.winner].name
            win_text = f"Ganador: {winner_name}"
            self.screen.blit(FONT_MED.render(win_text, True, GREEN), (10, self.window_h - 30))
        elif self.game.is_terminal():
            self.screen.blit(FONT_MED.render("Empate", True, BLACK), (10, self.window_h - 30))

        pygame.display.flip()

    def _draw_x(self, rect, color=BLUE, pad=8, stroke=3):
        pygame.draw.line(self.screen, color,
                         (rect.left + pad, rect.top + pad),
                         (rect.right - pad, rect.bottom - pad), stroke)
        pygame.draw.line(self.screen, color,
                         (rect.right - pad, rect.top + pad),
                         (rect.left + pad, rect.bottom - pad), stroke)

    def _draw_o(self, rect, color=RED, pad=8, stroke=3, radius=None):
        center = rect.center
        if radius is None:
            radius = (min(rect.width, rect.height) - pad * 2) // 2
        pygame.draw.circle(self.screen, color, center, radius, stroke)

    def _draw_conquered_mark(self, mark, color, rect):
        pad = int(rect.width * 0.12)
        stroke = max(8, int(rect.width * 0.08))

        if mark == "X":
            self._draw_x(rect, color=color, pad=pad, stroke=stroke)
        else:
            radius = (min(rect.width, rect.height) - pad * 2) // 2
            self._draw_o(rect, color=color, pad=pad, stroke=stroke, radius=radius)

    def human_move_action(self, mx, my):
        hit = self.pixel_to_move(mx, my)
        if hit is None:
            return
        br, bc, cr, cc = hit
        valid = self.game.get_valid_moves()
        if (br, bc, cr, cc) not in valid:
            return
        self.game.make_move(br, bc, cr, cc)
        self.check_winner()
        if not self.game.is_terminal():
            pygame.event.post(pygame.event.Event(pygame.USEREVENT + 1))

    def ai_move_for_player(self, player):
        if self.game.is_terminal():
            return

        t0 = time.time()
        fixed = self.game.turn % 2

        score, mv = minimax(
            self.game,
            player_id=fixed,
            fixed_player_id=fixed,
            depth=player.depth,
            max_player=True,
            use_alphabeta=player.use_alphabeta,
            eval_function=player.eval_fun,
        )

        t1 = time.time()
        self.total_time[fixed] += (t1 - t0)
        self.move_counts[fixed] += 1

        if mv is None:
            self.check_winner()
            self.running = False
            return

        br, bc, cr, cc = mv
        self.game.make_move(br, bc, cr, cc)

        mark = "X" if self.game.current_player() == O else "O"
        print(f"{player.name} ({mark}): ({br},{bc})->({cr},{cc}) score={round(score, 2)} time={round(t1 - t0, 3)}s")
        self.check_winner()

        if not self.headless and not self.game.is_terminal():
            pygame.event.post(pygame.event.Event(pygame.USEREVENT + 1))

    def save_result(self):
        if self.game.winner is None:
            winner_name = "Draw"
        else:
            winner_name = self.players[self.game.winner].name

        avg1 = self.total_time[0] / max(self.move_counts[0], 1)
        avg2 = self.total_time[1] / max(self.move_counts[1], 1)

        ResultCollection.add_result(
            winner=winner_name,
            avg_player1=avg1,
            avg_player2=avg2,
            depth1=getattr(self.players[0], "depth", 0),
            depth2=getattr(self.players[1], "depth", 0),
            use_alphabeta1=getattr(self.players[0], "use_alphabeta", False),
            use_alphabeta2=getattr(self.players[1], "use_alphabeta", False),
            evaluation1=getattr(self.players[0], "eval_fun", lambda g, p: 0).__name__
                if hasattr(self.players[0], "eval_fun") else "human",
            evaluation2=getattr(self.players[1], "eval_fun", lambda g, p: 0).__name__
                if hasattr(self.players[1], "eval_fun") else "human",
            total_player1=self.total_time[0],
            total_player2=self.total_time[1],
        )

    def check_winner(self):
        if self.game.is_terminal():
            self.save_result()
            if self.game.winner is not None:
                winner_name = self.players[self.game.winner].name
                print(f"Juego terminado! Ganador: {winner_name}")
            else:
                print("Juego terminado! Empate")
            avg1 = self.total_time[0] / max(self.move_counts[0], 1)
            avg2 = self.total_time[1] / max(self.move_counts[1], 1)
            print(f"Tiempo total Player 1: {round(self.total_time[0], 2)}s (promedio: {round(avg1, 4)}s)")
            print(f"Tiempo total Player 2: {round(self.total_time[1], 2)}s (promedio: {round(avg2, 4)}s)")
            self.running = False

    def run(self):
        if self.headless:
            while self.running and not self.game.is_terminal():
                current = self.players[self.game.turn % 2]
                self.ai_move_for_player(current)
            return

        while self.running:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    self.running = False
                elif ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_ESCAPE:
                        self.running = False
                elif ev.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    current = self.players[self.game.turn % 2]
                    if current.is_human and not self.game.is_terminal():
                        self.human_move_action(mx, my)
                elif ev.type == pygame.USEREVENT + 1:
                    current = self.players[self.game.turn % 2]
                    if not current.is_human:
                        self.ai_move_for_player(current)

            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
