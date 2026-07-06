# NO TOCAR

EMPTY = 0
X = 1
O = 2

CELL_SIZE = 50
MINI_GAP = 4
META_GAP = 12
MARGIN = 30

WHITE = (245, 245, 245)
BLACK = (30, 30, 30)
LIGHT = (220, 200, 180)
BLUE = (80, 120, 200)
RED = (200, 80, 80)
YELLOW = (230, 200, 60)
GREEN = (80, 200, 120)
GRAY = (180, 180, 180)

LINES = [
    [(0, 0), (0, 1), (0, 2)],
    [(1, 0), (1, 1), (1, 2)],
    [(2, 0), (2, 1), (2, 2)],
    [(0, 0), (1, 0), (2, 0)],
    [(0, 1), (1, 1), (2, 1)],
    [(0, 2), (1, 2), (2, 2)],
    [(0, 0), (1, 1), (2, 2)],
    [(0, 2), (1, 1), (2, 0)],
]


def check_three_in_a_row(grid):
    for line in LINES:
        vals = [grid[r][c] for r, c in line]
        if vals[0] != EMPTY and vals[0] == vals[1] == vals[2]:
            return vals[0]
    return EMPTY


class MiniBoard:
    def __init__(self):
        self.cells = [[EMPTY for _ in range(3)] for _ in range(3)]
        self.winner = EMPTY

    def is_full(self):
        return all(self.cells[r][c] != EMPTY for r in range(3) for c in range(3))

    def is_done(self):
        return self.winner != EMPTY or self.is_full()

    def place(self, r, c, player):
        if self.cells[r][c] != EMPTY or self.is_done():
            return False
        self.cells[r][c] = player
        self.winner = check_three_in_a_row(self.cells)
        return True

    def clone(self):
        mb = MiniBoard()
        mb.cells = [row[:] for row in self.cells]
        mb.winner = self.winner
        return mb


class Board:
    def __init__(self):
        self.mini_boards = [[MiniBoard() for _ in range(3)] for _ in range(3)]
        self.meta = [[EMPTY for _ in range(3)] for _ in range(3)]
        self.active_board = None

    def get_mini(self, br, bc):
        return self.mini_boards[br][bc]

    def update_meta(self, br, bc):
        self.meta[br][bc] = self.mini_boards[br][bc].winner

    def meta_winner(self):
        return check_three_in_a_row(self.meta)

    def is_meta_full(self):
        return all(self.mini_boards[r][c].is_done() for r in range(3) for c in range(3))

    def clone(self):
        b = Board()
        for br in range(3):
            for bc in range(3):
                b.mini_boards[br][bc] = self.mini_boards[br][bc].clone()
        b.meta = [row[:] for row in self.meta]
        b.active_board = self.active_board
        return b
