from board import EMPTY, X, O, LINES


def _player_mark(player_idx):
    return X if player_idx == 0 else O


def _count_two_in_a_row(grid, mark):
    count = 0
    for line in LINES:
        vals = [grid[r][c] for r, c in line]
        if vals.count(mark) == 2 and vals.count(EMPTY) == 1:
            count += 1
    return count


def _count_one_in_a_row(grid, mark):
    count = 0
    for line in LINES:
        vals = [grid[r][c] for r, c in line]
        if vals.count(mark) == 1 and vals.count(EMPTY) == 2:
            count += 1
    return count


def evaluate(game, player_idx):
    if game.winner is not None:
        return 1e9 if game.winner == player_idx else -1e9

    opp_idx = 1 - player_idx
    my_mark = _player_mark(player_idx)
    opp_mark = _player_mark(opp_idx)

    my_boards = 0
    opp_boards = 0
    my_cells = 0
    opp_cells = 0

    for br in range(3):
        for bc in range(3):
            mini = game.board.get_mini(br, bc)
            if mini.winner == my_mark:
                my_boards += 1
            elif mini.winner == opp_mark:
                opp_boards += 1
            for cr in range(3):
                for cc in range(3):
                    if mini.cells[cr][cc] == my_mark:
                        my_cells += 1
                    elif mini.cells[cr][cc] == opp_mark:
                        opp_cells += 1

    tempo = 0.01 if (game.turn % 2) == player_idx else -0.01
    score = 3.0 * (my_boards - opp_boards) + 0.1 * (my_cells - opp_cells) + tempo
    return score


def strategic_eval(game, player_idx):
    if game.winner is not None:
        return 1e9 if game.winner == player_idx else -1e9

    opp_idx = 1 - player_idx
    my_mark = _player_mark(player_idx)
    opp_mark = _player_mark(opp_idx)

    my_boards = 0
    opp_boards = 0
    my_mini_threats = 0
    opp_mini_threats = 0
    my_mini_ones = 0
    opp_mini_ones = 0

    for br in range(3):
        for bc in range(3):
            mini = game.board.get_mini(br, bc)
            if mini.winner == my_mark:
                my_boards += 1
            elif mini.winner == opp_mark:
                opp_boards += 1
            elif not mini.is_done():
                my_mini_threats += _count_two_in_a_row(mini.cells, my_mark)
                opp_mini_threats += _count_two_in_a_row(mini.cells, opp_mark)
                my_mini_ones += _count_one_in_a_row(mini.cells, my_mark)
                opp_mini_ones += _count_one_in_a_row(mini.cells, opp_mark)

    board_score = 5.0 * (my_boards - opp_boards)
    mini_threat_score = 0.6 * (my_mini_threats - opp_mini_threats)
    mini_ones_score = 0.15 * (my_mini_ones - opp_mini_ones)

    meta = game.board.meta
    my_meta_threats = _count_two_in_a_row(meta, my_mark)
    opp_meta_threats = _count_two_in_a_row(meta, opp_mark)
    meta_threat_score = 3.0 * (my_meta_threats - opp_meta_threats)

    my_meta_ones = _count_one_in_a_row(meta, my_mark)
    opp_meta_ones = _count_one_in_a_row(meta, opp_mark)
    meta_ones_score = 0.4 * (my_meta_ones - opp_meta_ones)

    tempo = 0.05 if (game.turn % 2) == player_idx else -0.05

    return (board_score + mini_threat_score + mini_ones_score +
            meta_threat_score + meta_ones_score + tempo)


# Aca defines tus funciones de evaluacion
def custom_eval(game, player_idx):
    if game.winner is not None:
        return 1e9 if game.winner == player_idx else -1e9

    opp_idx = 1 - player_idx
    my_mark = _player_mark(player_idx)
    opp_mark = _player_mark(opp_idx)

    my_boards = 0
    opp_boards = 0
    my_mini_threats = 0
    opp_mini_threats = 0
    my_mini_ones = 0
    opp_mini_ones = 0
    my_mini_forks = 0
    opp_mini_forks = 0

    for br in range(3):
        for bc in range(3):
            mini = game.board.get_mini(br, bc)
            if mini.winner == my_mark:
                my_boards += 1
            elif mini.winner == opp_mark:
                opp_boards += 1
            elif not mini.is_done():
                my_t = _count_two_in_a_row(mini.cells, my_mark)
                opp_t = _count_two_in_a_row(mini.cells, opp_mark)
                my_mini_threats += my_t
                opp_mini_threats += opp_t
                my_mini_ones += _count_one_in_a_row(mini.cells, my_mark)
                opp_mini_ones += _count_one_in_a_row(mini.cells, opp_mark)
                # Forks en los mini tableros
                if my_t >= 2:
                    my_mini_forks += 1
                if opp_t >= 2:
                    opp_mini_forks += 1

    meta = game.board.meta
    my_meta_threats = _count_two_in_a_row(meta, my_mark)
    opp_meta_threats = _count_two_in_a_row(meta, opp_mark)
    my_meta_ones = _count_one_in_a_row(meta, my_mark)
    opp_meta_ones = _count_one_in_a_row(meta, opp_mark)
    my_meta_fork  = 1 if my_meta_threats >= 2 else 0
    opp_meta_fork = 1 if opp_meta_threats >= 2 else 0

    # Todo lo de strategic_eval intacto
    board_score = 5.0 * (my_boards - opp_boards)
    mini_threat_score = 0.6 * (my_mini_threats - opp_mini_threats)
    mini_ones_score = 0.15 * (my_mini_ones - opp_mini_ones)
    meta_threat_score = 3.0 * (my_meta_threats - opp_meta_threats)
    meta_ones_score = 0.4 * (my_meta_ones - opp_meta_ones)
    tempo = 0.05 if (game.turn % 2) == player_idx else -0.05

    # Añadimos los forks nomas encima de lo que strategic eval estaba haciendo bien
    mini_fork_score = 1.5 * (my_mini_forks - opp_mini_forks)
    meta_fork_score = 10.0 * (my_meta_fork  - opp_meta_fork)

    return (board_score + mini_threat_score + mini_ones_score +
            meta_threat_score + meta_ones_score + tempo +
            mini_fork_score + meta_fork_score)
