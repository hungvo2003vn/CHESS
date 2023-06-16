import pygame as pg
import sys
from pygame.locals import *
from SETTING import *
from UI import *
from chessBoard import *

# Init pygame
pg.init()
pg.display.set_caption("Chess")

display_screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


#Font size
MEDIUM_FONT = pg.font.Font("OpenSans-Regular.ttf", 28)
LARGE_FONT = pg.font.Font("OpenSans-Regular.ttf", 40)
MOVE_FONT = pg.font.Font("OpenSans-Regular.ttf", 60)

def main():

    #Init user and AI
    CHESS_GAME = ChessBoard()
    game_over = True

    # POSITION MOUSE
    start_row = None
    start_col = None

    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
        
        display_screen.fill(BLACK)

        if CHESS_GAME.user is None:
            StartUp(display_screen, CHESS_GAME, LARGE_FONT, MEDIUM_FONT)

        else:
            
            # Display the updated board
            CHESS_GAME.make_board_all(display_screen)
            pos = None
            
            # Display the choosen area
            if len(CHESS_GAME.sqClick) == 1:
                HighlighRect(display_screen, start_col, start_row)
            
            ############ User's turn ############
            # Check if pieces is clicked
            if CHESS_GAME.ai_turn == False:
                
                # Create Title
                X_content = (X_BOARD + BOARD_LENGTH*CELL_SIZE + SCREEN_WIDTH)/2
                Y_content = (SCREEN_HEIGHT)/2
                CreateTitle(display_screen, X_content, Y_content, 0, 0, "Your turn", LARGE_FONT)

                # Check if pieces is clicked
                for event in pg.event.get():
                    if event.type == QUIT:
                        pg.quit()
                        sys.exit()
                    elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        pos = pg.mouse.get_pos()
                
                if pos is not None:
                    pos, start_row, start_col = CHESS_GAME.CheckingClicked(pos)

            ############ AI's turn ############
            else:
                # Create Title
                X_content = (X_BOARD + BOARD_LENGTH*CELL_SIZE + SCREEN_WIDTH)/2
                Y_content = (SCREEN_HEIGHT)/2
                content = "AI's turn" + "..."
                
                CreateTitle(display_screen, X_content, Y_content, 0, 0, content, LARGE_FONT)

                # Check if pieces is clicked
                for event in pg.event.get():
                    if event.type == QUIT:
                        pg.quit()
                        sys.exit()
                    elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        pos = pg.mouse.get_pos()
                
                if pos is not None:
                    pos, start_row, start_col = CHESS_GAME.CheckingClicked(pos)


            ############ GAME OVER ############
            if game_over:
                
                content = "Play Again"
                width = SCREEN_WIDTH/6
                height = 50
                x = (X_BOARD + BOARD_LENGTH*CELL_SIZE + SCREEN_WIDTH)/2 - (width)/2
                y = (SCREEN_HEIGHT)/2 + 50
                game_over_button = CreateButton(display_screen, x, y, width, height, content, MEDIUM_FONT)

                # Check if button is clicked
                click, _, _ = pg.mouse.get_pressed()
                if click == 1:
                    mouse = pg.mouse.get_pos()
                    if game_over_button.collidepoint(mouse):
                        time.sleep(0.2)
                        CHESS_GAME = ChessBoard()
                    
                    
            
        # Update after each event
        pg.display.update()

if __name__ == "__main__":
    main()