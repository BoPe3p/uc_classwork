# minimax.py
import random

NEG_INF = float("-inf")
POS_INF = float("inf")


def _eval_terminal_or_heur(game, fixed_player_id, eval_function):
    # NO TOCAR
    if game.winner is not None:
        return POS_INF if game.winner == fixed_player_id else NEG_INF
    return eval_function(game, fixed_player_id)


def minimax(game, player_id, fixed_player_id, depth, max_player, use_alphabeta, eval_function, alpha=NEG_INF, beta=POS_INF):
    # Caso base: profundidad 0 o estado terminal
    if depth == 0 or game.is_terminal():
        return _eval_terminal_or_heur(game, fixed_player_id, eval_function), None

    moves = game.get_valid_moves()
    if not moves:
        return _eval_terminal_or_heur(game, fixed_player_id, eval_function), None

    random.shuffle(moves)

    is_max = (game.turn % 2) == fixed_player_id
    best_score = NEG_INF if is_max else POS_INF
    best_move = moves[0]

    for mv in moves:
        g2 = game.clone()
        br, bc, cr, cc = mv
        ok = g2.make_move(br, bc, cr, cc)
        if not ok:
            continue

        if g2.winner is not None:
            if g2.winner == fixed_player_id:
                return POS_INF, mv
            score = NEG_INF
        else:
            score, _ = minimax(g2, 1 - player_id, fixed_player_id, depth - 1, not is_max, use_alphabeta, eval_function, alpha, beta)

        if is_max:
            if score > best_score:
                best_score = score
                best_move = mv
        else:
            if score < best_score:
                best_score = score
                best_move = mv

        # Poda alfa-beta
        if use_alphabeta:
            # Vemos si es necesario actualizar alpha o beta
            if is_max:
                if score > alpha:
                    alpha = score
            
            else:
                if score < beta:
                    beta = score
            
            # Si se cumple esto, se poda
            if beta <= alpha:
                break    
            

    return best_score, best_move
