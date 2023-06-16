from SETTING import *
import pygame as pg
from pygame.locals import *
import copy

############## CLASS of MOVE ##############
class Move:

    def __init__(self, start_pos, end_pos, PIECES_MAP, white_turn):

        self.startRow = start_pos[0]
        self.startCol = start_pos[1]
        self.endRow = end_pos[0]
        self.endCol = end_pos[1]
        self.PIECES_MAP = copy.deepcopy(PIECES_MAP)
        self.white_turn = white_turn

        return
    
    def isStayed(self):

        return self.startRow == self.endRow and self.startCol == self.endCol
    
    def ValidStartMove(self):

        return self.PIECES_MAP[self.startRow][self.startCol] != "--"
    
    def ValidClick(self):

        return (self.startRow in range(0, BOARD_LENGTH) and self.startCol in range(0, BOARD_LENGTH)) and (self.endRow in range(0, BOARD_LENGTH) and self.endCol in range(0, BOARD_LENGTH))
            
    def InsideBoard(self, row, col):
        return (row in range(0, BOARD_LENGTH) and col in range(0, BOARD_LENGTH))

    def Movement(self, row, col, step, type):

        if type == "U":
            return [row - step, col]
        elif type == "D":
            return [row + step, col]
        elif type == "L":
            return [row, col - step]
        elif type == "R":
            return [row, col + step]
        elif type == "UR":
            return [row - step, col + step]
        elif type == "UL":
            return [row - step, col - step]
        elif type == "DR":
            return [row + step, col + step]
        elif type == "DL":
            return [row + step, col - step]
        
        return [row, col]

    # Pawn
    def PawnMoves(self, ai_turn):

        PossibleMoves = []
        # Get current color's turn
        color = self.PIECES_MAP[self.startRow][self.startCol][0] # Current color

        #User turn
        if ai_turn == False:
            
            if self.startRow == 6:
                if self.PIECES_MAP[5][self.startCol] == "--" and self.PIECES_MAP[4][self.startCol] == "--":
                    PossibleMoves += [[self.startRow - 2, self.startCol]]


            UpMove = self.Movement(self.startRow, self.startCol, 1, "U")
            UpLeft = self.Movement(self.startRow, self.startCol, 1, "UL")
            UpRight = self.Movement(self.startRow, self.startCol, 1, "UR")

            #Collect UpMove
            if self.InsideBoard(UpMove[0], UpMove[1]) and self.PIECES_MAP[UpMove[0]][UpMove[1]] == "--":
                PossibleMoves += [UpMove]
            
            #Collect UpLeft
            if self.InsideBoard(UpLeft[0], UpLeft[1]):

                if self.PIECES_MAP[UpLeft[0]][UpLeft[1]] != "--":
                    if color != self.PIECES_MAP[UpLeft[0]][UpLeft[1]][0]:
                        PossibleMoves += [UpLeft]

            #Collect UpRight
            if self.InsideBoard(UpRight[0], UpRight[1]):

                if self.PIECES_MAP[UpRight[0]][UpRight[1]] != "--":
                    if color != self.PIECES_MAP[UpRight[0]][UpRight[1]][0]:
                        PossibleMoves += [UpRight]
        
        # AI turn
        if ai_turn:
            
            if self.startRow == 1:
                if self.PIECES_MAP[2][self.startCol] == "--" and self.PIECES_MAP[3][self.startCol] == "--":
                    PossibleMoves += [[self.startRow + 2, self.startCol]]


            DownMove = self.Movement(self.startRow, self.startCol, 1, "D")
            DownLeft = self.Movement(self.startRow, self.startCol, 1, "DL")
            DownRight = self.Movement(self.startRow, self.startCol, 1, "DR")

            #Collect DownMove
            if self.InsideBoard(DownMove[0], DownMove[1]) and self.PIECES_MAP[DownMove[0]][DownMove[1]] == "--":
                PossibleMoves += [DownMove]
            
            #Collect DownLeft
            if self.InsideBoard(DownLeft[0], DownLeft[1]):

                if self.PIECES_MAP[DownLeft[0]][DownLeft[1]] != "--":
                    if color != self.PIECES_MAP[DownLeft[0]][DownLeft[1]][0]:
                        PossibleMoves += [DownLeft]

            #Collect UpRight
            if self.InsideBoard(DownRight[0], DownRight[1]):

                if self.PIECES_MAP[DownRight[0]][DownRight[1]] != "--":
                    if color != self.PIECES_MAP[DownRight[0]][DownRight[1]][0]:
                        PossibleMoves += [DownRight]
        

        return PossibleMoves
    
    # King
    def KingMoves(self):

        PossibleMoves = []
        # Get current color's turn
        color = self.PIECES_MAP[self.startRow][self.startCol][0] # Current color

        UpMove = self.Movement(self.startRow, self.startCol, 1, "U")
        UpLeft = self.Movement(self.startRow, self.startCol, 1, "UL")
        UpRight = self.Movement(self.startRow, self.startCol, 1, "UR")

        LeftMove = self.Movement(self.startRow, self.startCol, 1, "L")
        RightMove = self.Movement(self.startRow, self.startCol, 1, "R")

        DownMove = self.Movement(self.startRow, self.startCol, 1, "D")
        DownLeft = self.Movement(self.startRow, self.startCol, 1, "DL")
        DownRight = self.Movement(self.startRow, self.startCol, 1, "DR")

        case_moves = [UpMove, UpLeft, UpRight, LeftMove, RightMove, DownMove, DownLeft, DownRight]

        for moves in case_moves:
            if self.InsideBoard(moves[0], moves[1]) and color != self.PIECES_MAP[moves[0]][moves[1]][0]:
                PossibleMoves += [moves]
        
        return PossibleMoves
    
    # Queen
    def QueenMoves(self):

        PossibleMoves = []
        # Get current color's turn
        color = self.PIECES_MAP[self.startRow][self.startCol][0] # Current color

        able_continue_moving = [True, True, True, True, True, True, True, True]

        for step in range(1, BOARD_LENGTH):
            
            UpMove = self.Movement(self.startRow, self.startCol, step, "U")
            UpLeft = self.Movement(self.startRow, self.startCol, step, "UL")
            UpRight = self.Movement(self.startRow, self.startCol, step, "UR")

            LeftMove = self.Movement(self.startRow, self.startCol, step, "L")
            RightMove = self.Movement(self.startRow, self.startCol, step, "R")

            DownMove = self.Movement(self.startRow, self.startCol, step, "D")
            DownLeft = self.Movement(self.startRow, self.startCol, step, "DL")
            DownRight = self.Movement(self.startRow, self.startCol, step, "DR")

            case_moves = [UpMove, UpLeft, UpRight, LeftMove, RightMove, DownMove, DownLeft, DownRight]

            for idx in range(len(case_moves)):
                moves = case_moves[idx]

                if self.InsideBoard(moves[0], moves[1]) and color != self.PIECES_MAP[moves[0]][moves[1]][0] and able_continue_moving[idx]:
                    PossibleMoves += [moves]
                else:
                    able_continue_moving[idx] = False

        return PossibleMoves
    
    # Rook
    def RookMoves(self):

        PossibleMoves = []
        # Get current color's turn
        color = self.PIECES_MAP[self.startRow][self.startCol][0] # Current color

        able_continue_moving = [True, True, True, True]

        for step in range(1, BOARD_LENGTH):
            
            UpMove = self.Movement(self.startRow, self.startCol, step, "U")
            LeftMove = self.Movement(self.startRow, self.startCol, step, "L")
            RightMove = self.Movement(self.startRow, self.startCol, step, "R")
            DownMove = self.Movement(self.startRow, self.startCol, step, "D")

            case_moves = [UpMove, LeftMove, RightMove, DownMove]

            for idx in range(len(case_moves)):
                moves = case_moves[idx]

                if self.InsideBoard(moves[0], moves[1]) and color != self.PIECES_MAP[moves[0]][moves[1]][0] and able_continue_moving[idx]:
                    PossibleMoves += [moves]
                else:
                    able_continue_moving[idx] = False

        return PossibleMoves
                
    # Bishop
    def BishopMoves(self):

        PossibleMoves = []
        # Get current color's turn
        color = self.PIECES_MAP[self.startRow][self.startCol][0] # Current color

        able_continue_moving = [True, True, True, True]

        for step in range(1, BOARD_LENGTH):
            
            UpLeft = self.Movement(self.startRow, self.startCol, step, "UL")
            UpRight = self.Movement(self.startRow, self.startCol, step, "UR")
            DownLeft = self.Movement(self.startRow, self.startCol, step, "DL")
            DownRight = self.Movement(self.startRow, self.startCol, step, "DR")

            case_moves = [UpLeft, UpRight, DownLeft, DownRight]

            for idx in range(len(case_moves)):
                moves = case_moves[idx]

                if self.InsideBoard(moves[0], moves[1]) and color != self.PIECES_MAP[moves[0]][moves[1]][0] and able_continue_moving[idx]:
                    PossibleMoves += [moves]
                else:
                    able_continue_moving[idx] = False

        return PossibleMoves

    # Knight
    def KnightMoves(self):

        PossibleMoves = []
        # Get current color's turn
        color = self.PIECES_MAP[self.startRow][self.startCol][0] # Current color

        Rtan_21 = [-2, 1]
        Rtan_12 = [-1, 2]
        Rtan_12_neg = [1, 2]
        Rtan_21_neg = [2, 1]

        Ltan_21 = [-2, -1]
        Ltan_12 = [-1, -2]
        Ltan_12_neg = [1, -2]
        Ltan_21_neg = [2, -1]

        case_moves = [Rtan_21, Rtan_12, Rtan_12_neg, Rtan_21_neg, Ltan_21, Ltan_12, Ltan_12_neg, Ltan_21_neg]

        for cases in case_moves:
            moves = [self.startRow + cases[0], self.startCol + cases[1]]

            if self.InsideBoard(moves[0], moves[1]) and color != self.PIECES_MAP[moves[0]][moves[1]][0]:
                PossibleMoves += [moves]
        
        return PossibleMoves


    # Summary valid function
    def isValidMove(self, ai_turn):

        if self.ValidClick() == False or self.isStayed() or self.ValidStartMove() == False:
            return False
        
        # Get current color's turn
        color_of_current = self.PIECES_MAP[self.startRow][self.startCol][0]
            
        if color_of_current == 'w' and self.white_turn == False:
            return False
        
        if color_of_current == 'b' and self.white_turn:
            return False
        
        # Check current pieces
        pieces_name = self.PIECES_MAP[self.startRow][self.startCol][1]

        if pieces_name == 'p':
            return [self.endRow, self.endCol] in self.PawnMoves(ai_turn)
        
        if pieces_name == 'K':
            return [self.endRow, self.endCol] in self.KingMoves()
        
        if pieces_name == 'Q':
            return [self.endRow, self.endCol] in self.QueenMoves()

        if pieces_name == 'R':
            return [self.endRow, self.endCol] in self.RookMoves()
        
        if pieces_name == 'B':
            return [self.endRow, self.endCol] in self.BishopMoves()
        
        if pieces_name == 'N':
            return [self.endRow, self.endCol] in self.KnightMoves()
        
        return True