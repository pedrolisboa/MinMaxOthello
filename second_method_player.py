from second_evaluation_method import *
from FrameworkTabuleiro.board import Board

class second_method_player:
    def __init__(self, color,wheights, corner_w):
        self.color = color
        if color == Board.WHITE:
            self.opponent = Board.BLACK
        else:
            self.opponent = Board.WHITE

    def evaluator(self,board):
        W_COINS, W_MOBILITY, W_CORNER, W_STABILITY = 0, 1, 2, 3
        max_player = self.color
        min_player = self.opponent
        return self.wheights[W_COINS] * coin_parity(board, max_player, min_player) + \
               self.wheights[W_MOBILITY] * mobility(board, max_player, min_player) * + \
               self.wheights[W_CORNER] * corner_mobility(board, max_player, min_player, self.corner_weights) + \
               self.wheights[W_STABILITY] * stability(board, max_player, min_player) / (self.wheights[W_COINS] +
                                                                                        self.wheights[W_CORNER] +
                                                                                        self.wheights[W_MOBILITY] +
                                                                                        self.wheights[W_STABILITY])

    def fs_alphabeta(self,move,stateBoard, depth, alpha, beta, search_counter,player_max):
        #from copy import copy

        copyState = stateBoard.get_clone()
        if search_counter:
            copyState.play(move, self.color)

        def debug_print():
            if ~(len(copyState.valid_moves(self.color))) or depth == 0:
                return
            return

        movesequence = []
        if ~len((copyState.valid_moves(self.color))) and search_counter:
            movesequence += [move]
            return self.evaluator(copyState), movesequence

        debug_print()
        movesequence = []

        if player_max: # MAX
            value = float('-inf')
            for move in stateBoard.valid_moves(self.color):
                child_value, child_movesequence = self.fs_alphabeta(move,copyState, depth-1, alpha, beta,search_counter + 1,False)
                value = max(value, child_value)

                if child_value >= alpha:
                    alpha = child_value
                    #movesequence = copy(child_movesequence)
                    movesequence = [move]

                if beta <= alpha:
                    break

        else:  # player_min
            value = float('inf')
            for move in stateBoard.valid_moves(self.color):
                child_value, child_movesequence = self.fs_alphabeta(move,copyState, depth - 1, alpha, beta, search_counter + 1, True)
                value = min(value, child_value)

                if child_value <= beta:
                    beta = child_value
                    #movesequence = copy(child_movesequence)
                    movesequence = [move]

                if beta <= alpha:
                    break

        debug_print()
        return value, movesequence[0]


    def play(self, board):
        return self.chooseNextMove(board)

    def chooseNextMove(self, stateBoard):
        #from models.move import Move
        _, bestMove = self.fs_alphabeta(0,stateBoard,10, float('-inf'), float('inf'), 0, True)
        #print bestMove
        return bestMove