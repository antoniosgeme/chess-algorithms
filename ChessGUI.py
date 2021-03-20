import pygame as p 
import ChessEngine
import sys

board_width = board_height = 800
board_dimension = 8
square_size = board_height // board_dimension
fps = 15
images = {}




def main():
    
        
    p.init()
    screen = p.display.set_mode((board_width,board_height))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    game_state = ChessEngine.GameState(True)
    load_lichess_images()
    squares_selected = ()
    last_two_player_clicks = []
    
    
    move_made = False
    game_over = False
    undone = False
    running = True
    while running:
        for e in p.event.get():
                if e.type == p.QUIT:
                     p.display.quit()
                     running = False
                     sys.exit()
                elif e.type == p.MOUSEBUTTONDOWN:
                    if not game_over:
                        location = p.mouse.get_pos()
                        col = location[0] // square_size
                        row = location[1] // square_size
                        if squares_selected == (row,col):
                            squares_selected = ()
                            last_two_player_clicks = []   
                        else:
                            squares_selected = (row,col)
                            last_two_player_clicks.append(squares_selected) 
                        if len(last_two_player_clicks) == 2: #After second click
                            start_square =  (7 - last_two_player_clicks[0][0]) * 8 + last_two_player_clicks[0][1]
                            end_square = (7 - last_two_player_clicks[1][0]) * 8 + last_two_player_clicks[1][1]
                            move = ChessEngine.chess.Move(start_square,end_square)
                            if move in game_state.board.legal_moves:
                                game_state.board.push(move)
                                move_made = True
                                squares_selected = ()
                                last_two_player_clicks = []
                            if not move_made:
                                last_two_player_clicks = [squares_selected]
                        
                elif e.type ==  p.KEYDOWN and game_state.board.move_stack:
                    if e.key == p.K_z: # Undo when z is pressed
                        game_state.board.pop()
                        move_made = True
                    if e.key == p.K_r:
                        game_state.board.reset()
                        squares_selected = ()
                        last_two_player_clicks = []
                        move_made = False
                        game_over = False
            
        draw_current_board(screen,game_state)
        clock.tick(fps)
        p.display.flip()
        
    
def draw_current_board(screen,game_state):
     draw_empty_board(screen)
     draw_pieces(screen,game_state)
     
def draw_pieces(screen,game_state):
    for color in [ChessEngine.chess.WHITE, ChessEngine.chess.BLACK]:
        for piece in range(1,7):
            if color:
                title = "w" + ChessEngine.chess.piece_symbol(piece).upper()
            else:
                title = "b" + ChessEngine.chess.piece_symbol(piece).upper()
                
            for square in list(game_state.board.pieces(piece,color)):
                c = square % board_dimension
                r = board_dimension - 1 - square // board_dimension
                screen.blit(images[title],p.Rect(c*square_size,r*square_size,square_size,square_size))

                
            
def highlight_squares(screen,game_state,squares_selected):
    if squares_selected != ():
        r,c = squares_selected
        if game_state.board[r][c][0] == ("w" if gs.whiteToMove else "b"):
            s = p.Surface((square_size,square_size))
            s.set_alpha(100)
            s.fill(p.Color("blue"))
            screen.blit(s,(c*square_size,r*square_size))
            s.fill(p.Color("yellow"))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s,(move.endCol*SQ_SIZE,move.endRow*SQ_SIZE))
    
    

def load_lichess_images():
    pieces = ["wP","wR","wN","wB","wK","wQ","bP","bR","bN","bB","bK","bQ"]
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (square_size,square_size))
        
def draw_empty_board(screen):
    global colors
    colors = [p.Color("burlywood1"), p.Color("chocolate3")]
    for r in range(board_dimension):
        for c in range(board_dimension):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen,color,p.Rect(c*square_size,r*square_size,square_size,square_size))


if __name__ == "__main__":
    main()




