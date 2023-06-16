from SETTING import *
import pygame as pg
from pygame.locals import *
from chessMove import *
import copy

class ChessBoard:

    def __init__ (self):

        self.CHESS_BOARD = None
        self.PIECES_MAP = copy.deepcopy(PIECES_MAP)
        self.flipped = False
        self.white_turn = False

        self.user = None
        self.ai_turn = False
        self.sqClick = []
        self.sqSelected = []
        
    def make_board(self, display_screen):
        # Draw board
        self.CHESS_BOARD = pg.surface.Surface((CELL_SIZE * BOARD_LENGTH, CELL_SIZE * BOARD_LENGTH))
        self.CHESS_BOARD.fill(BROWN)

         # Draw CELL
        for y in range(0, BOARD_LENGTH, 1):
            for x in range(0,BOARD_LENGTH, 1):
                if (x+y)%2 == 1:
                    pg.draw.rect(self.CHESS_BOARD, LIGHT_BROWN, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE) )

        display_screen.blit(self.CHESS_BOARD, (X_BOARD, Y_BOARD))

        return

    def load_pieces_img(self):

        PIECES_IMG = {}

        for pieces in PIECES:
            PIECES_IMG[pieces] = pg.image.load("img/pieces/"+ pieces + ".png")
            PIECES_IMG[pieces] =pg.transform.scale(PIECES_IMG[pieces], (CELL_SIZE, CELL_SIZE))

        return PIECES_IMG
    
    def load_pieces_map(self, display_screen):

        PIECES_IMG = self.load_pieces_img()
        if self.user == "BLACK" and self.flipped == False:
            self.flip_chess_map()
            self.flipped = True

        for y in range(0, BOARD_LENGTH, 1):
            for x in range(0,BOARD_LENGTH, 1):

                if self.PIECES_MAP[y][x] != "--":

                    pieces = self.PIECES_MAP[y][x]
                    display_screen.blit(PIECES_IMG[pieces], (x*CELL_SIZE + X_BOARD, y*CELL_SIZE + Y_BOARD, CELL_SIZE, CELL_SIZE))
        return
    
    #Flip color white to black:
    def flip_chess_map(self):

        self.PIECES_MAP[0:2], self.PIECES_MAP[-1:-3 :-1] = self.PIECES_MAP[-1:-3:-1], self.PIECES_MAP[0:2]

        return
    
    # Summary board
    def make_board_all(self, display_screen):

        self.make_board(display_screen)
        self.load_pieces_map(display_screen)

        return
    
    # Make move
    def make_move(self, move):
        
        if move.isValidMove(self.ai_turn) == False:
            return
        
        self.PIECES_MAP[move.endRow][move.endCol] = self.PIECES_MAP[move.startRow][move.startCol]
        self.PIECES_MAP[move.startRow][move.startCol] = "--"

    # Cheking clicked and make_move
    def CheckingClicked(self, pos):
    
        start_col = (int)((pos[0] - X_BOARD) // CELL_SIZE)
        start_row = (int)((pos[1] - Y_BOARD) // CELL_SIZE)

        if Valid_HighlighRect(start_col, start_col):

            # Store move
            self.sqSelected = [start_row, start_col]
            self.sqClick.append(self.sqSelected)
            print(self.sqSelected)
            print(self.sqClick)
            
            # Make move
            if len(self.sqClick) == 2:

                player_move = Move(self.sqClick[0], self.sqClick[1], self.PIECES_MAP, self.white_turn)
                self.make_move(player_move)

                self.sqSelected = []
                self.sqClick = []

                if player_move.isValidMove(self.ai_turn):
                    self.setPlayer()
        
        else:
            self.sqSelected = []
            self.sqClick = []
        
        return pos, start_row, start_col
    
    # check current player
    def setPlayer(self):

        self.ai_turn = not self.ai_turn
        self.white_turn = not self.white_turn

        return
    

def Valid_HighlighRect(x, y):

    return (x in range(0, BOARD_LENGTH) and y in range(0, BOARD_LENGTH))