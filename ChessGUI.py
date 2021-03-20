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
    image_dict = {}
    
    
    running = True
    while running:
        for e in p.event.get():
                if e.type == p.QUIT:
                     p.display.quit()
                     running = False
                     sys.exit()
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




