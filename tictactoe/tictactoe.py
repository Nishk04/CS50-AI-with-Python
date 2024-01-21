"""
Tic Tac Toe Player
"""

import copy
import math

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
    # Count the number of X's and O's on the board
    count_X = sum(row.count('X') for row in board)
    count_O = sum(row.count('O') for row in board)

    if terminal(board):
        return None

    if count_X <= count_O:
        return X
    else:
        return O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    if terminal(board):
        return ValueError("Terminal Board has been reached in the function: actions")
    
    possible_actions = set()
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == EMPTY:
                possible_actions.add((row, col))
    return possible_actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("Not valid action in function: result")
    row, col = action
    board_copy = copy.deepcopy(board)
    board_copy[row][col] = player(board)
    return board_copy

def check_row(board, player):
    for row in range(len(board)):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            return True
    return False # No winner horizontally

def check_col(board, player):
    # Basically you could write i in range 3 meaning it iterates: 0, 1, 2
    for col in range(len(board)):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            return True
    return False
            
def check_diagnol(board, player):
    row = 0
    count = 0
    for col in range(len(board[0])):
        if board[row][col] == player and row == col:
            count += 1
            row += 1
        if count == 3:
            return True
    else:
        return False

def check_diagnol2(board, player):
    row = 2  # Start at the last row
    count = 0
    for col in range(len(board[0])):
        if board[row][col] == player:
            count += 1
        row -= 1 
        if count == 3:
            return True
    else:
        return False

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if check_row(board, X) or check_col(board, X) or check_diagnol(board, X) or check_diagnol2(board, X): return X
    elif check_row(board, O) or check_col(board, O) or check_diagnol(board, O) or check_diagnol2(board, O): return O
    else: return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == X or winner(board) == O:
        return True
    count_final = sum(row.count(X) for row in board)
    if count_final == 5:
        return True
    return False
    
def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X: return 1
    elif winner(board) == O: return -1
    else: return 0
# Max and Min value function return a utility after going down one sequence of moves until the terminal state
def max_value(board):
    v = -math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v

def min_value(board):
    v = math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v

def minimax(board):
    """ Returns the optimal action for the current player on the board. """
    if terminal(board):
        return None
    elif player(board) == X:
        plays = []
        for action in actions(board):
            plays.append([min_value(result(board, action)), action])
        return sorted(plays, key=lambda x: x[0], reverse = True)[0][1]
    elif player(board) == O:
        plays = []
        for action in actions(board):
            plays.append([max_value(result(board, action)), action])
        # We want to play the winning move for O if there is one
        '''if any(utility(result(board, action)) == -1 for action in actions(board)):
            return plays.append([max_value(result(board, action)), action])'''
        return sorted(plays, key=lambda x: x[0])[0][1] # Basically accesing the first pair in player
        # These last two brackets access player[utility, action] so the first number: the utility
        # then the second number which the action with that utility
                             
