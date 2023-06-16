from SETTING import *
import pygame as pg
from pygame.locals import *
import time

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

def HighlighRect(display_screen, x, y):

    if Valid_HighlighRect(x, y) == False:
        return 
    
    x = x*CELL_SIZE + X_BOARD
    y = y*CELL_SIZE + Y_BOARD

    pg.draw.rect(display_screen, GREEN_YELLOW, pg.Rect(x, y, CELL_SIZE, CELL_SIZE), 2)


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
