from copy import copy
import numpy as np

"""
:Usage
    >>> import minmax
    >>> alphabeta(node, depth, -INFINITY, +INFINITY, heuristic_fun, child_gen_fun, counter, TRUE/FALSE)

:param
    state: initial node of the search
    alpha: alpha value for max player
    beta: beta value for min player
    evaluate: calculate the node value
    is_endgame:function to evaluate terminal game conditions
    gen_children: generator of next states
    search_counter: counter for presentation of search results
    player_max: boolean value to indicate the level player: TRUE = max, FALSE = min

:return value associated with the node
"""
def fs_alphabeta(state, depth, alpha, beta, evaluate, gen_children, is_endgame, search_counter, player_max):
    def debug_print():
        if is_endgame(state) or depth == 0:
            print(search_counter, end='  | \t' * search_counter)
            print('[', state,end='\t'*2),
            print('Value: ', end='')
            print("\t", evaluate(state),end=']\n')
            return
        print(search_counter, end='  | \t' * search_counter)
        print('[', state, end='\t'*2),
        print('Alpha: ',alpha, end='\t')
        print('Beta: ',beta, end=']\n')
        return

    if is_endgame(state):
        movesequence = np.array(state)
        return evaluate(state), movesequence

    debug_print()
    movesequence = np.empty(0)
    if player_max:
        value = float('-inf')
        for child in gen_children(copy(state)):
            child_value,child_movesequence = fs_alphabeta(child, depth - 1, alpha, beta, evaluate,
                                                          gen_children, is_endgame, search_counter + 1, False)
            value = max(value, child_value)

            if child_value >= alpha:
                alpha = child_value
                movesequence = np.append(child_movesequence, state)

            if beta <= alpha:
                break

    else:  # player_min
        value = float('inf')
        for child in gen_children(copy(state)):
            child_value,child_movesequence = fs_alphabeta(child, depth - 1, alpha, beta, evaluate,
                                                          gen_children, is_endgame, search_counter + 1, True)
            value = min(value, child_value)

            if child_value <= beta:
                beta = child_value
                movesequence = np.append(child_movesequence, state)

            if beta <= alpha:
                break

    debug_print()
    return value, movesequence

