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

    # Title 
    X_content = (X_BOARD + BOARD_LENGTH*CELL_SIZE + SCREEN_WIDTH)/2
    Y_content = (SCREEN_HEIGHT)/2
    content = None

    while True:

        #Update the display_screen
        pg.display.update()

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
            
            # Display the choosen area of opponent
            if CHESS_GAME.ai_turn is False and len(CHESS_GAME.Move_logs) > 0:

                latest_move = CHESS_GAME.Move_logs[-1][1][1]
                ai_row, ai_col = latest_move[0], latest_move[1]
                HighlighRect(display_screen, ai_col, ai_row, RED, 5)
                    
            # Display the choosen area of user
            if len(CHESS_GAME.sqClick) == 1:
                HighlighRect(display_screen, start_col, start_row, GREEN_YELLOW, 2)

                last_click = Move([start_row, start_col], [0,0], CHESS_GAME.PIECES_MAP, CHESS_GAME.white_turn)
                pieces = CHESS_GAME.PIECES_MAP[start_row][start_col]
                all_poss = last_click.AllPossibleMoves(pieces, CHESS_GAME.ai_turn)
                for y,x in all_poss:
                    HighlighRect(display_screen, x, y, GREEN_YELLOW, 5)
            
            # Get Winner
            AGENT = Agent(CHESS_GAME.PIECES_MAP, CHESS_GAME.white_turn, CHESS_GAME.ai_turn, CHESS_GAME.Move_logs)
            Winner = AGENT.winner()

            ############ Checking Game over ############
            game_over = AGENT.terminated()

            if game_over:
                if Winner != "BLACK" and Winner != "WHITE":
                    content = f"Tie! - {Winner}"
                elif Winner == CHESS_GAME.user:
                    content = "You Win!"
                else:
                    content = "You lose!"
                
                CreateTitle(display_screen, X_content, Y_content, 0, 0, content, LARGE_FONT)

            ############ GAME OVER ############
            CHESS_GAME = GameOver_Button(display_screen, CHESS_GAME, MEDIUM_FONT)
            # Undo Button
            CHESS_GAME = Undo_Button(display_screen, CHESS_GAME, MEDIUM_FONT)

            if not game_over:

                ############ User's turn ############
                if CHESS_GAME.ai_turn == False:
                    
                    # Create Title
                    content = "Your turn"
                    CreateTitle(display_screen, X_content, Y_content, 0, 0, content, LARGE_FONT)
                    pg.display.update()

                    # Check if pieces is clicked
                    for event in pg.event.get():
                        if event.type == QUIT:
                            pg.quit()
                            sys.exit()
                        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                            pos = pg.mouse.get_pos()
                    
                    if pos is not None:
                        pos, start_row, start_col = CHESS_GAME.CheckingClicked(pos)
                    
                    # if CHESS_GAME.ai_turn:
                    #     CHESS_GAME.make_board_all(display_screen)
                    
                    # # AI automatic
                    # best_move = minimax(CHESS_GAME.PIECES_MAP, CHESS_GAME.white_turn, CHESS_GAME.ai_turn, CHESS_GAME.Move_logs)
                    # ai_move = Move(best_move[0], best_move[1], CHESS_GAME.PIECES_MAP, CHESS_GAME.white_turn)
                    
                    # CHESS_GAME.make_move(ai_move)
                    # CHESS_GAME.setPlayer()

                ############ AI's turn ############
                else:
                    
                    # Create Title
                    content = "AI's turn..."
                    CreateTitle(display_screen, X_content, Y_content, 0, 0, content, LARGE_FONT)
                    pg.display.update()
                    
                    # Make decision
                    time.sleep(0.5)
                    best_move = minimax(CHESS_GAME.PIECES_MAP, CHESS_GAME.white_turn, CHESS_GAME.ai_turn, CHESS_GAME.Move_logs)
                    ai_move = Move(best_move[0], best_move[1], CHESS_GAME.PIECES_MAP, CHESS_GAME.white_turn)
                    
                    CHESS_GAME.make_move(ai_move)
                    CHESS_GAME.setPlayer()
            
        # Update after each event
        # pg.display.update()

if __name__ == "__main__":
    main()