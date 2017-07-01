class FirstMethodPlayer:
    def __init__(self, color):
        self.color = color

    def evaluator(self, stateBoard):
        weights = [10,801.724,382.026,78.922,74.396,10]
        b = 0
        w = 0
        value = 0
        for i in range(1,9):
            for j in range(1,9):
                if (stateBoard.get_square_color(i,j) == stateBoard.WHITE):
                    w += 1
                elif (stateBoard.get_square_color(i,j) == stateBoard.BLACK):
                    b += 1
        # Piece Difference
        if b > w:
            p = 100 * b / (b + w)
        elif b < w:
            p = -100 * b / (b + w)
        else:  # B==W
            p = 0
        # Mobility
        m = p
        if (~b | ~w):
            m = 0
        # Frontier Discs
        f = -p
        # Corner Occupancy
        c = 25 * b - 25 * w
        # Corner Closeness
        l = -12.5 * b + 12.5 * w
        # Disc squares
        V = [[20, -3, 11, 8],[-3, -7, -4, 1],[11, -4, 2, 2],[8, 1 , 2, -3]]
        d=0
        for line in range(1,9):
            for col in range(1,9):
                i=line-1
                j=col-1
                sigma=0
                if line>4:
                    i=-line+8
                if col>4:
                    j=-col+8
                if stateBoard.get_square_color(line,col) == stateBoard.WHITE:
                    sigma = -1
                elif stateBoard.get_square_color(line,col) == stateBoard.BLACK:
                    sigma = 1
                d+=sigma*V[i][j]
        ck = [p, c, l, m, f, d]
        value = 0
        for n in range(len(ck)):
            value+=ck[n]*weights[n]
        return value


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
