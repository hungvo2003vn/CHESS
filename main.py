import pygame as pg
import sys
from pygame.locals import *
from SETTING import *
from UI import *
from chessBoard import *
from chessEngine import *

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
    game_over = False

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
                HighlighRect(display_screen, start_col, start_row, GREEN_YELLOW, 2)
            
            if CHESS_GAME.ai_turn is False:
                
                if len(CHESS_GAME.Move_logs) > 0:
                    latest_move = CHESS_GAME.Move_logs[-1][1][1]
                    ai_row, ai_col = latest_move[0], latest_move[1]
                    HighlighRect(display_screen, ai_col, ai_row, RED, 5)

            ############ Checking Game over ############
            game_over = terminated(CHESS_GAME.PIECES_MAP, CHESS_GAME.white_turn, CHESS_GAME.ai_turn, CHESS_GAME.Move_logs)
            
            if game_over:

                # Create Title
                X_content = (X_BOARD + BOARD_LENGTH*CELL_SIZE + SCREEN_WIDTH)/2
                Y_content = (SCREEN_HEIGHT)/2
                Winner = winner(CHESS_GAME.PIECES_MAP, CHESS_GAME.white_turn, CHESS_GAME.ai_turn, CHESS_GAME.Move_logs)
                content = None
                if Winner is None:
                    content = "Game Over: Tie!"
                elif Winner == CHESS_GAME.user:
                    content = "You Win!"
                else:
                    content = "You lose!"

                CreateTitle(display_screen, X_content, Y_content, 0, 0, content, LARGE_FONT)
                # Undo Button
                CHESS_GAME = Undo_Button(display_screen, CHESS_GAME, MEDIUM_FONT)
            
            ############ User's turn ############
            # Check if pieces is clicked
            if CHESS_GAME.ai_turn == False:
                
                # Undo Button
                CHESS_GAME = Undo_Button(display_screen, CHESS_GAME, MEDIUM_FONT)
                
                if not game_over:
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

                if not game_over:
                    
                    # Create Title
                    X_content = (X_BOARD + BOARD_LENGTH*CELL_SIZE + SCREEN_WIDTH)/2
                    Y_content = (SCREEN_HEIGHT)/2
                    content = "AI's turn" + "..."
                    
                    CreateTitle(display_screen, X_content, Y_content, 0, 0, content, LARGE_FONT)

                    # Check if pieces is clicked
                    # for event in pg.event.get():
                    #     if event.type == QUIT:
                    #         pg.quit()
                    #         sys.exit()
                    #     elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    #         pos = pg.mouse.get_pos()
                    
                    # if pos is not None:
                    #     pos, start_row, start_col = CHESS_GAME.CheckingClicked(pos)
                    
                    Possible_actions = actions(CHESS_GAME.PIECES_MAP, CHESS_GAME.white_turn, CHESS_GAME.ai_turn)
                    best_move = random.choice(Possible_actions)

                    #best_move = minimax(CHESS_GAME.PIECES_MAP, CHESS_GAME.white_turn, CHESS_GAME.ai_turn, CHESS_GAME.Move_logs)
                    ai_move = Move(best_move[0], best_move[1], CHESS_GAME.PIECES_MAP, CHESS_GAME.white_turn)
                    
                    CHESS_GAME.make_move(ai_move)
                    CHESS_GAME.setPlayer()

                    
            ############ GAME OVER ############
            CHESS_GAME = GameOver_Button(display_screen, CHESS_GAME, MEDIUM_FONT)
                    
            
        # Update after each event
        pg.display.update()

if __name__ == "__main__":
    main()