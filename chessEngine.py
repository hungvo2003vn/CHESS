from SETTING import *
from pygame.locals import *
from chessMove import *
import copy
import random

# Always use the deepcopy

########## Helper function for winner ##########
def isStaleMate(board, white_turn, ai_turn):

    color = None
    if white_turn:
        color = 'w'
    else:
        color = 'b'

    # Traverse through the board
    for row in range(BOARD_LENGTH):
        for col in range(BOARD_LENGTH):

            pieces = board[row][col]
            if pieces[0] != color:
                continue
            
            move = Move([row, col], [0, 0], board, white_turn)
            PossibleMoves = move.AllPossibleMoves(pieces, ai_turn)

            if PossibleMoves != []:
                return False

    return True

def isCheckMate(board, white_turn):

    kingCheck = None
    if white_turn:
        kingCheck = "wK"
    else:
        kingCheck = "bK"

    #Traverse through the board
    if any(kingCheck in row for row in board):
        return False

    return True

def isTie(Move_logs):

    # Check for a tie based on the 50-move rule
    consecutive_non_capture_moves = 0

    for move in Move_logs:

        piece = move[0][0] #Piece of the start_pos

        if "p" in piece:  # Check if the piece is a pawn
            consecutive_non_capture_moves = 0
        elif "p" not in piece:  # Check if the piece is not a pawn
            consecutive_non_capture_moves += 1
        
        if consecutive_non_capture_moves >= 50:
            return True  # Game ended in a tie due to the 50-move rule

    return False


# King vs king with no other pieces.
# King and bishop vs king.
# King and knight vs king.
# King and bishop vs king and bishop of the same coloured square.

# King and two knights vs king.
# King and rook vs king and rook.
# King and rook vs king and bishop or king and knight.

def get_bishop_color(bishop):
    # Get the color of the bishop based on its position
    row, col = bishop[1]
    if (row + col) % 2 == 0:
        return "Light"
    else:
        return "Dark"

def has_insufficient_material(board):
    # Count the number of pieces for each player
    white_pieces = []
    black_pieces = []

    for row in board:
        for piece in row:
            if piece[0] == 'w':
                white_pieces.append(piece)
            elif piece[0] == 'b':
                black_pieces.append(piece)

    # Check for insufficient material
    insufficient_material = False

    if len(white_pieces) == 1 and len(black_pieces) == 1:
        # Only kings remaining for both players
        insufficient_material = True

    elif len(white_pieces) == 2 and len(black_pieces) == 1:
        # King and bishop vs king
        if any(piece == "wB" for piece in white_pieces):
            insufficient_material = True

    elif len(white_pieces) == 2 and len(black_pieces) == 2:
        # King and bishop vs king and bishop of the same colored square
        white_bishop = next((piece for piece in white_pieces if piece == "wB"), None)
        black_bishop = next((piece for piece in black_pieces if piece == "bB"), None)

        if white_bishop and black_bishop:
            white_bishop_color = get_bishop_color(white_bishop)
            black_bishop_color = get_bishop_color(black_bishop)

            if white_bishop_color == black_bishop_color:
                insufficient_material = True

    elif len(white_pieces) == 2 and len(black_pieces) == 3:
        # King and knight vs king
        if any(piece == "wN" for piece in white_pieces):
            insufficient_material = True

    elif len(white_pieces) == 3 and len(black_pieces) == 2:
        # King and bishop vs king and bishop of the same colored square
        white_bishop = next((piece for piece in white_pieces if piece == "wB"), None)
        black_bishop = next((piece for piece in black_pieces if piece == "bB"), None)

        if white_bishop and black_bishop:
            white_bishop_color = get_bishop_color(white_bishop)
            black_bishop_color = get_bishop_color(black_bishop)

            if white_bishop_color == black_bishop_color:
                insufficient_material = True

    elif len(white_pieces) == 3 and len(black_pieces) == 3:
        # King and two knights vs king
        if any(piece == "wN" for piece in white_pieces) and len(white_pieces) == 3:
            insufficient_material = True

    elif len(white_pieces) == 3 and len(black_pieces) == 4:
        # King and rook vs king and bishop or king and knight
        white_rook = next((piece for piece in white_pieces if piece == "wR"), None)
        black_bishop = next((piece for piece in black_pieces if piece == "bB"), None)
        black_knight = next((piece for piece in black_pieces if piece == "bN"), None)

        if white_rook and (black_bishop or black_knight):
            insufficient_material = True

    return insufficient_material


########## Main function for Minimax Algorithm ##########
def winner(board, white_turn, ai_turn, Move_logs):

    if isTie(Move_logs):
        return "50R"
    
    if isCheckMate(board, white_turn):
        if white_turn:
            return "BLACK"
        else:
            return "WHITE"
    
    if isStaleMate(board, white_turn, ai_turn):
        return "STM"
    
    if has_insufficient_material(board):
        return "IM"
    
    return None

def terminated(board, white_turn, ai_turn, Move_logs):

    if Move_logs == []:
        return False
    
    Winner = winner(board, white_turn, ai_turn, Move_logs)
    
    if Winner is not None:
        return True

    return False

def actions(board, white_turn, ai_turn):

    PossibleActions = []
    color = None
    if white_turn:
        color = 'w'
    else:
        color = 'b' 
    
    for row in range(BOARD_LENGTH):
        for col in range(BOARD_LENGTH):
            
            pieces = board[row][col]
            if color != pieces[0]:
                continue

            move = Move([row, col], [0, 0], board, white_turn)
            PossibleMoves = move.AllPossibleMoves(pieces, ai_turn)
            if PossibleMoves == []:
                continue
            
            start_pos = [row, col]
            for end_pos in PossibleMoves:
                PossibleActions += [[start_pos, end_pos]]

    return PossibleActions

def add_to_Move_logs(board, move, Move_logs):

    start_pos = move[0]
    start_pieces = board[start_pos[0]][start_pos[1]]

    end_pos = move[1]
    end_pieces = board[end_pos[0]][end_pos[1]]

    new_Move_logs = copy.deepcopy(Move_logs)
    new_Move_logs += [   [[start_pieces, start_pos], [end_pieces, end_pos]]   ]

    return new_Move_logs

def result(board, move, Move_logs): #[start, end]

    new_Move_logs = add_to_Move_logs(board, move, Move_logs)

    new_board = copy.deepcopy(board)
    start_pos = move[0]
    end_pos = move[1]

    new_board[end_pos[0]][end_pos[1]] = new_board[start_pos[0]][start_pos[1]]
    new_board[start_pos[0]][start_pos[1]] = "--"

    if new_board[end_pos[0]][end_pos[1]][1] == 'p':

        if end_pos[0] == 0 or end_pos[0] == (BOARD_LENGTH - 1):
            color = new_board[end_pos[0]][end_pos[1]][0]
            new_board[end_pos[0]][end_pos[1]] = color + 'Q'
    
    return new_board, new_Move_logs



def utility(board, white_turn, ai_turn, Move_logs):

    Winner = winner(board, white_turn, ai_turn, Move_logs)
    if Winner == "White": # Max player
        return 1
    elif Winner == "Black": # Min player
        return -1
    
    return 0

def minimax(board, white_turn, ai_turn, Move_logs):

    optimal_action = None

    alpha = -INF
    beta = INF

    if white_turn:
        optimal_action = max_player(board, white_turn, ai_turn, Move_logs)[1]
    else:
        optimal_action = min_player(board, white_turn, ai_turn, Move_logs)[1]
    
    return optimal_action


def max_player(board, white_turn, ai_turn, Move_logs, min_value = INF, depth = DEPTH):
    
    Possible_actions = actions(board, white_turn, ai_turn)
    best_move = random.choice(Possible_actions)
    max_value = -INF

    if depth == 0 or terminated(board, white_turn, ai_turn, Move_logs):
        return [utility(board, white_turn, ai_turn, Move_logs), None]

    while len(Possible_actions) > 0:

        if max_value >= min_value:
            break

        move = random.choice(Possible_actions)
        Possible_actions.remove(move)
        next_board, next_Move_logs = result(board, move, Move_logs)

        next_player_set = min_player(next_board, not white_turn, not ai_turn, next_Move_logs, max_value, depth - 1)
        if max_value < next_player_set[0]:
            max_value = next_player_set[0]
            best_move = move

    return [max_value, best_move]

    

def min_player(board, white_turn, ai_turn, Move_logs, max_value = -INF, depth = DEPTH):
    
    Possible_actions = actions(board, white_turn, ai_turn)
    best_move = random.choice(Possible_actions)
    min_value = INF

    if depth == 0 or terminated(board, white_turn, ai_turn, Move_logs):
        return [utility(board, white_turn, ai_turn, Move_logs), None]


    while len(Possible_actions) > 0:

        if max_value >= min_value:
            break

        move = random.choice(Possible_actions)
        Possible_actions.remove(move)
        next_board, next_Move_logs = result(board, move, Move_logs)

        next_player_set = max_player(next_board, not white_turn, not ai_turn, next_Move_logs, min_value, depth - 1)

        if min_value > next_player_set[0]:
            min_value = next_player_set[0]
            best_move = move

    return [max_value, best_move]
    