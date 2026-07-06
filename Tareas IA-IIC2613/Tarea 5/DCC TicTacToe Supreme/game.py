# NO TOCAR
from board import Board, EMPTY, X, O

POSITION_WEIGHTS = {
    (1, 1): 3,
    (0, 0): 2, (0, 2): 2, (2, 0): 2, (2, 2): 2,
    (0, 1): 1, (1, 0): 1, (1, 2): 1, (2, 1): 1,
}


def player_to_index(player):
    return 0 if player == X else 1


def index_to_player(idx):
    return X if idx == 0 else O


def opponent_mark(player):
    return O if player == X else X


class Game:
    def __init__(self):
        self.board = Board()
        self.turn = 0
        self.winner = None  # None, 0 (player X), or 1 (player O)

    def current_player(self):
        return X if self.turn % 2 == 0 else O

    def current_player_index(self):
        return self.turn % 2

    def get_valid_moves(self):
        if self.winner is not None:
            return []

        moves = []
        ab = self.board.active_board

        if ab is not None:
            br, bc = ab
            mini = self.board.get_mini(br, bc)
            if not mini.is_done():
                for cr in range(3):
                    for cc in range(3):
                        if mini.cells[cr][cc] == EMPTY:
                            moves.append((br, bc, cr, cc))
                return moves

        for br in range(3):
            for bc in range(3):
                mini = self.board.get_mini(br, bc)
                if mini.is_done():
                    continue
                for cr in range(3):
                    for cc in range(3):
                        if mini.cells[cr][cc] == EMPTY:
                            moves.append((br, bc, cr, cc))
        return moves

    def make_move(self, br, bc, cr, cc):
        player = self.current_player()
        mini = self.board.get_mini(br, bc)

        if mini.is_done() or mini.cells[cr][cc] != EMPTY:
            return False

        if self.board.active_board is not None:
            abr, abc = self.board.active_board
            if (abr, abc) != (br, bc):
                return False

        mini.place(cr, cc, player)

        # Regla de Robo: si el mini-tablero se lleno sin ganador,
        # se lo lleva el rival del ultimo jugador que puso ficha
        if mini.winner == EMPTY and mini.is_full():
            stolen_by = opponent_mark(player)
            mini.winner = stolen_by

        self.board.update_meta(br, bc)

        mw = self.board.meta_winner()
        if mw != EMPTY:
            self.winner = player_to_index(mw)
        elif self.board.is_meta_full():
            self.winner = self._weighted_tiebreak()

        next_mini = self.board.get_mini(cr, cc)
        if next_mini.is_done():
            self.board.active_board = None
        else:
            self.board.active_board = (cr, cc)

        self.turn += 1
        return True

    def _weighted_tiebreak(self):
        x_score = 0
        o_score = 0
        for (r, c), weight in POSITION_WEIGHTS.items():
            owner = self.board.meta[r][c]
            if owner == X:
                x_score += weight
            elif owner == O:
                o_score += weight

        if x_score > o_score:
            return 0
        elif o_score > x_score:
            return 1

        # Ultimo desempate: dueno del centro
        center = self.board.meta[1][1]
        if center == X:
            return 0
        elif center == O:
            return 1
        return None

    def is_terminal(self):
        if self.winner is not None:
            return True
        if len(self.get_valid_moves()) == 0:
            self.winner = self._weighted_tiebreak()
            return True
        return False

    def clone(self):
        g = Game()
        g.board = self.board.clone()
        g.turn = self.turn
        g.winner = self.winner
        return g

    def result(self):
        return self.winner
