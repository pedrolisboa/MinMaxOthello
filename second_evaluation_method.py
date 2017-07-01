from FrameworkTabuleiro import board
from FrameworkTabuleiro.move import Move


########################################################
# MISCELLANEOUS
########################################################

def eval_heuristic(eval_max, eval_min):
    if eval_max + eval_min != 0:
        return 100 * (eval_max - eval_min) / \
               (eval_max + eval_min)
    return 0


def get_diagonal(board, i, j, orientation):
    return [board[(i + i - 1) % len(board)][(j + orientation * i - 1) % len(board[0])] for i in range(len(board))]


def check_line_fillings(board, direction="row"):
    lines = []
    if direction == "row":
        for i in range(1, 9):
            if '.' in board[i][:]:
                lines += [1]
            else:
                lines += [0]
    elif direction == "col":
        for i in range(1, 9):
            if '.' in board[:][i]:
                lines += [1]
            else:
                lines += [0]
    elif direction == "diagLR":
        for i in range(1, 9):
            if '.' in get_diagonal(board, 1, i, 1):
                lines += [1]
            else:
                lines += [0]
    elif direction == "diagRL":
        for i in range(1, 9):
            if '.' in get_diagonal(board, 1, i, -1):
                lines += [1]
            else:
                lines += [0]
    return lines


##########################################################################

def coin_parity(board, max_player, min_player):
    coin_count = lambda board, player_color: sum([1 if (board.get_square_color(i, j) == player_color)
                                                  else 0 for i in range(0, 9) for j in range(0, 9)]
                                                 )

    max_player_coins = coin_count(board, max_player)
    min_player_coins = coin_count(board, min_player)

    return eval_heuristic(max_player_coins, min_player_coins)


"""
:param
"""


def mobility(board, max_player, min_player):
    max_player_actual_mob = len(board.valid_moves(max_player))
    min_player_actual_mob = len(board.valid_moves(min_player))

    # MOBILIDADE POTENCIAL NAO IMPLEMENTADA
    return eval_heuristic(max_player_actual_mob, min_player_actual_mob)


def corner_mobility(board, max_player, min_player, wheights):
    def get_player_potential_corners(player_moves):
        return sum([1 if (mov == Move(i, j)) else 0 for mov in player_moves
                    for i in [1, 8] for j in [1, 8]])

    def get_player_corner_pieces(board, player_piece):
        return sum([1 if (board.get_square_color(i, j) == player_piece)
                    else 0 for i in [1, 8] for j in [1, 8]])

    # Calculate corner values for each player
    max_player_actual_corners = get_player_corner_pieces(board, max_player)
    max_player_potential_corners = get_player_potential_corners(board.valid_moves(max_player))
    max_player_unlikely_corners = 4 - max_player_potential_corners

    min_player_actual_corners = get_player_corner_pieces(board, min_player)
    min_player_potential_corners = get_player_potential_corners(board.valid_moves(max_player))
    min_player_unlikely_corners = 4 - min_player_potential_corners

    # Calculate heuristic blocks
    heuristic_actual_corners = eval_heuristic(max_player_actual_corners,
                                              min_player_actual_corners)
    heuristic_potential_corners = eval_heuristic(max_player_potential_corners,
                                                 min_player_potential_corners)
    heuristic_unlikely_corners = eval_heuristic(max_player_unlikely_corners, min_player_unlikely_corners)

    W_ACTUAL, W_POTENTIAL, W_UNLIKELY = 0, 1, 2
    return (wheights[W_ACTUAL] * heuristic_actual_corners +
            wheights[W_POTENTIAL] * heuristic_potential_corners +
            wheights[W_UNLIKELY] * heuristic_unlikely_corners) / (
               wheights[W_ACTUAL] + wheights[W_POTENTIAL] + wheights[W_UNLIKELY])


def stability(board, max_player, min_player):
    def evaluate_stab_row_col(board, rows, cols, max_player, min_player, i):
        max_stab = 0
        min_stab = 0
        if rows[i] == 0:
            if board[i][1] == max_player:
                max_stab += 1
            else:
                min_stab += 1
        if cols[i] == 0:
            if board[1][i] == min_player:
                max_stab += 1
            else:
                min_stab += 1
        return max_stab, min_stab

    def evaluate_stab_diags(board, diagsLR, diagsRL, max_player, min_player, i, j):
        max_stab = 0
        min_stab = 0
        if diagsLR[j] == 0:
            if board[i][j] == max_player:
                max_stab += 1
            else:
                min_stab += 1
        if diagsRL[-j] == 0:
            if board[i][j] == min_player:
                max_stab += 1
            else:
                min_stab += 1
        return max_stab, min_stab

    rows = check_line_fillings(board, "row")
    cols = check_line_fillings(board, "col")
    diagsLR = check_line_fillings(board, "diagLR")
    diagsRL = check_line_fillings(board, "diagRL")

    max_stability = 0
    min_stability = 0
    for i in range(1, 9):
        tmp_max_stab, tmp_min_stab = evaluate_stab_row_col(board, rows, cols, max_player, min_player, i)
        max_stability += tmp_max_stab
        min_stability += tmp_min_stab
        for j in range(1, 9):
            tmp_max_stab, tmp_min_stab = evaluate_stab_diags(board,
                                                             rows, cols, max_player, min_player, i, j)
            max_stability += tmp_max_stab
            min_stability += tmp_min_stab

            # Check for enemy positions in the neighborhood
            # Boolean for max dominance in the adjacent squares
            max_neib = True
            # Boolean for min dominance in the adjacent squares
            min_neib = True

            for offsetX in [-1, 0, 1]:
                for offsetY in [-1, 0, 1]:
                    if board[i + offsetX][j + offsetY] != max_player:
                        max_neib = False
                        max_stability -= 1
                        break
            if ~max_neib:
                for offsetX in [-1, 0, 1]:
                    for offsetY in [-1, 0, 1]:
                        if board[i + offsetX][j + offsetY] != min_player:
                            min_neib = False
                            break
            else:
                max_stability += 1
            if min_neib:
                min_stability += 1

    return eval_heuristic(max_stability, min_stability)




board_stamp = [['.' for i in range(0, 10)] for j in range(0, 10)]
newBoard = board.Board(board_stamp)
newMove = Move(5, 3)
newBoard.play(newMove, newBoard.BLACK)
newMove = Move(5, 4)
newBoard.play(newMove, newBoard.WHITE)
newMove = Move(5, 5)
newBoard.play(newMove, newBoard.BLACK)
newMove = Move(4, 5)
newBoard.play(newMove, newBoard.WHITE)
newMove = Move(4, 4)
newBoard.play(newMove, newBoard.BLACK)
newMove = Move(6, 3)
newBoard.play(newMove, newBoard.WHITE)
newMove = Move(6, 2)
newBoard.play(newMove, newBoard.BLACK)
newMove = Move(6, 1)
newBoard.play(newMove, newBoard.WHITE)
newMove = Move(7, 1)
newBoard.play(newMove, newBoard.BLACK)
print(newBoard)
offset = 4
for i in [row[-(i + offset + 2)] for i, row in enumerate(newBoard.board[-1:][-1:]) if
          0 <= i + offset + 2 < len(newBoard.board)]:
    print(i)
# print(len(newBoard.valid_moves(newBoard.WHITE)))
# print(len(newBoard.valid_moves(newBoard.BLACK)))
print(corner_mobility(newBoard, newBoard.BLACK, newBoard.WHITE, [1, 1, 1]))
# print(len(newBoard.valid_moves(newBoard.BLACK)))
# print(coin_parity(newBoard, newBoard.BLACK, newBoard.WHITE))
