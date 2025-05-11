"""
Tic Tac Toe Player
"""

import copy

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns player who has the next turn on a board.
    """

    x_count = 0
    o_count = 0

    #look and keep track of each cell
    for row in range(3):
        for cell in range(3):
            if board[row][cell] == X:
                x_count += 1
            elif board[row][cell] == O:
                o_count += 1

    #decide who's turn it is
    if x_count > o_count:
        return O
    else:
        return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    available = set()

    #check what cells are empty, if so append to available
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                available.add((i, j))

    return available

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    row = action[0]
    cell = action[1]
    if row < 0:
        raise NameError('Invalid Move!')
    if cell < 0:
        raise NameError('Invalid Move!')
    if row > 2:
        raise NameError('Invalid Move!')
    if cell > 2:
        raise NameError('Invalid Move!')

    #check to see if desired move is valid
    if board[row][cell] is not EMPTY:
        raise NameError('Invalid Move!')

    #create a copy of the board
    board_copy = copy.deepcopy(board)

    #change the copy according to the action
    board_copy[row][cell] = player(board)

    return board_copy

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    for num in range(3):

        #check for horizontal win cases
        if board[num][0] == board[num][1] == board[num][2] != EMPTY:
            return board[num][0]

        #check for verticle win cases
        elif board[0][num] == board[1][num] == board[2][num] != EMPTY:
            return board[0][num]

    #check for diagonal win cases
    if board[0][0] == board [1][1] == board[2][2] != EMPTY:
        return board[0][0]
    elif board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]

    #if no one wins return none
    else:
        return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    full = True

    #look over board to see if full, if not return false
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                full = False

    for square in range(3):
        #check for horizontal terminal cases
        if board[square][0] == board[square][1] == board[square][2] != EMPTY:
            return True

        #check for verticle terminal cases
        elif board[0][square] == board[1][square] == board[2][square] != EMPTY:
            return True

    #check for diagonal cases
    if board[0][0] == board [1][1] == board[2][2] != EMPTY:
        return True

    elif board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return True

    # check for a tie case
    elif full is True:
        return True

    else:
        return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

#adapted from lecture 0's slideshow (slides #285, #286)

    #function to maximize score
    def max_value(board, alpha, beta):

        #check if the board is already a terminal case
        if terminal(board):
            return (utility(board), None, float('inf'), utility(board))

        v = float('-inf')

        for action in actions(board):
            minimum = min_value(result(board, action), alpha, beta) #call min_value to search deeper
            if minimum[0] > v:
                v = minimum[0]

                #perform alpha-beta pruning
                alpha = max(minimum[2], minimum[3], alpha)
                best = action

                #check for prune case
                if alpha >= beta:
                    break

        return (v, best, alpha, beta)

    #function to minimize score
    def min_value(board,alpha, beta):

        #check if the board is already a terminal case
        if terminal(board):
            return (utility(board), None, utility(board), float('-inf'))

        v = float('inf')

        for action in actions(board):
            maximum = max_value(result(board, action), alpha, beta) #call max_value to search deeper
            if maximum[0] < v:
                v = maximum[0]

                #perform alpha-beta pruning
                beta = min(maximum[2], maximum[3], beta)
                best = action

                #check for prune case
                if alpha >= beta:
                    break

        return (v, best, alpha, beta)

    if terminal(board):
        return None

    #call max_val or min_val first if X or O
    if player(board) == X:
        move = max_value(board, float('-inf'), float('inf'))
        return move[1]

    if player(board) == O:
        move = min_value(board, float('-inf'), float('inf'))
        return move[1]
