from SETTING import *
import pygame as pg
from pygame.locals import *
import time
from chessBoard import*

############## FUNCTION of STARTUP SCREEN ##############

def CreateButton(display_screen, x, y, width, height, content, font):

    Button = pg.Rect(x, y, width, height)

    play_content = font.render(content, True, BLACK)
    play_content_Rect = play_content.get_rect()
    play_content_Rect.center = Button.center

    pg.draw.rect(display_screen, WHITE, Button)
    display_screen.blit(play_content, play_content_Rect)

    return Button

def CreateTitle(display_screen, x, y, width, height, content, font):

    Title = font.render(content, True, WHITE)

    Title_Rect = Title.get_rect()
    Title_Rect.center = (x, y)
    display_screen.blit(Title, Title_Rect)

    return Title

def HighlighRect(display_screen, x, y, color, line_width):

    if Valid_HighlighRect(x, y) == False:
        return 
    
    x = x*CELL_SIZE + X_BOARD
    y = y*CELL_SIZE + Y_BOARD

    pg.draw.rect(display_screen, color, pg.Rect(x, y, CELL_SIZE, CELL_SIZE), line_width)


def StartUp(display_screen, CHESS_GAME, LARGE_FONT, MEDIUM_FONT):

    # Create Startup Screen
    CreateTitle(display_screen, (SCREEN_WIDTH/2), 50, 0,0, "CHESS GAME", LARGE_FONT)
    play_white = CreateButton(display_screen, (SCREEN_WIDTH/8), (SCREEN_HEIGHT/2), SCREEN_WIDTH/4, 50, "Play White", MEDIUM_FONT)
    play_black = CreateButton(display_screen, 5*(SCREEN_WIDTH/8), (SCREEN_HEIGHT/2), SCREEN_WIDTH/4, 50, "Play Black", MEDIUM_FONT)

    # Check if button is clicked
    click, _, _ = pg.mouse.get_pressed()
    if click == 1:
        mouse = pg.mouse.get_pos()
        if play_white.collidepoint(mouse):
            time.sleep(0.2)
            CHESS_GAME.user = "WHITE"
            CHESS_GAME.white_turn = True
        elif play_black.collidepoint(mouse):
            time.sleep(0.2)
            CHESS_GAME.user = "BLACK"

    return

def Valid_HighlighRect(x, y):

    return (x in range(0, BOARD_LENGTH) and y in range(0, BOARD_LENGTH))


def GameOver_Button(display_screen, CHESS_GAME, MEDIUM_FONT):

    content = "Play Again"
    width = SCREEN_WIDTH/6
    height = 50
    x = (X_BOARD + BOARD_LENGTH*CELL_SIZE + SCREEN_WIDTH)/2 - (width)/2
    y = (SCREEN_HEIGHT)/2 + 100
    game_over_button = CreateButton(display_screen, x, y, width, height, content, MEDIUM_FONT)

    # Check if button is clicked
    click, _, _ = pg.mouse.get_pressed()
    if click == 1:
        mouse = pg.mouse.get_pos()
        if game_over_button.collidepoint(mouse):
            time.sleep(0.2)
            CHESS_GAME = ChessBoard()

    return CHESS_GAME

def Undo_Button(display_screen, CHESS_GAME, MEDIUM_FONT):

    content = "Undo Move"
    width = SCREEN_WIDTH/6
    height = 50
    x = (X_BOARD + BOARD_LENGTH*CELL_SIZE + SCREEN_WIDTH)/2 - (width)/2
    y = (SCREEN_HEIGHT)/2 + 40
    game_over_button = CreateButton(display_screen, x, y, width, height, content, MEDIUM_FONT)

    # Check if button is clicked
    click, _, _ = pg.mouse.get_pressed()
    if click == 1:
        mouse = pg.mouse.get_pos()
        if game_over_button.collidepoint(mouse):
            time.sleep(0.2)
            CHESS_GAME.undo_move()
            CHESS_GAME.undo_move()

    return CHESS_GAME