import pygame as p 
import ChessEngine
import sys

board_width = board_height = 800
board_dimension = 8
square_size = board_height // board_dimension
fps = 15
images = {}
piece_dict = {"Q" : ChessEngine.chess.QUEEN,
              "R" : ChessEngine.chess.ROOK,
              "B" : ChessEngine.chess.BISHOP,
              "N" : ChessEngine.chess.KNIGHT}

def main():
    choice = input("Would you like to play with the white pieces or the black pieces? (W/B) : ")
    #HumanVsHuman(choice.upper() =="W")
    HumanVsEngine(choice.upper() =="W")
    
def HumanVsEngine(play_with_white:bool):
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
    running = True
    human_to_move = True if play_with_white else False
    while running:
        if human_to_move:
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
                            start_square =  convert_square(last_two_player_clicks[0],play_with_white)
                            end_square = convert_square(last_two_player_clicks[1],play_with_white)
                            promote_to = None
                            if game_state.board.piece_type_at(start_square) == ChessEngine.chess.PAWN:
                                if (ChessEngine.chess.square_rank(end_square) == 7 or 
                                    ChessEngine.chess.square_rank(end_square) == 0):
                                    promote_to = ChessEngine.chess.QUEEN
                            move = ChessEngine.chess.Move(start_square,end_square,promotion=promote_to)
                            if move in game_state.board.legal_moves:
                                if promote_to != None :
                                    promote_piece = input("What would you like to promote to? (Q,R,B,N) : ")
                                    try:
                                        promote_to = piece_dict[promote_piece.upper()]
                                    except:
                                        promote_piece = input("Oops! Please try again. What would you like to promote to? (Q,R,B,N) : ")
                                    move = ChessEngine.chess.Move(start_square,end_square,promotion=promote_to)
                                game_state.board.push(move)
                                human_to_move = False
                                move_made = True
                                squares_selected = ()
                                last_two_player_clicks = []
                            if not move_made:
                                last_two_player_clicks = [squares_selected]   
                elif e.type ==  p.KEYDOWN and game_state.board.move_stack:
                    if e.key == p.K_z: # Undo when z is pressed
                        game_state.board.pop()
                        game_state.board.pop()
                        move_made = True
                        human_to_move = True
                    if e.key == p.K_r:
                        game_state.board.reset()
                        squares_selected = ()
                        last_two_player_clicks = []
                        move_made = False
                        game_over = False
                        human_to_move = True if play_with_white else False
        else:
            if not game_over:
                move = game_state.make_move()
                game_state.board.push(move)
                move_made = True
                human_to_move = True
                
        if move_made:
            move_made = False
        draw_current_board(screen,game_state,squares_selected,play_with_white)
        if game_state.board.is_checkmate():
            game_over = True
            human_to_move = True
            if game_state.board.turn:   
                drawText(screen,"Black Wins by Checkmate!")
            else: 
                drawText(screen,"White Wins by Checkmate!")
        elif game_state.board.is_stalemate():
            game_over = True
            human_to_move = True
            drawText(screen,"Stalemate")
        clock.tick(fps)
        p.display.flip()     





def HumanVsHuman(play_with_white: bool):
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
                        start_square =  convert_square(last_two_player_clicks[0],play_with_white)
                        end_square = convert_square(last_two_player_clicks[1],play_with_white)
                        promote_to = None
                        if game_state.board.piece_type_at(start_square) == ChessEngine.chess.PAWN:
                            if (ChessEngine.chess.square_rank(end_square) == 7 or 
                                ChessEngine.chess.square_rank(end_square) == 0):
                                promote_to = ChessEngine.chess.QUEEN
                        move = ChessEngine.chess.Move(start_square,end_square,promotion=promote_to)
                        if move in game_state.board.legal_moves:
                            if promote_to != None :
                                promote_piece = input("What would you like to promote to? (Q,R,B,N) : ")
                                try:
                                    promote_to = piece_dict[promote_piece.upper()]
                                except:
                                    promote_piece = input("Oops! Please try again. What would you like to promote to? (Q,R,B,N) : ")
                                move = ChessEngine.chess.Move(start_square,end_square,promotion=promote_to)
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
        if move_made:
            move_made = False
        draw_current_board(screen,game_state,squares_selected,play_with_white)
        if game_state.board.is_checkmate():
            game_over = True
            if game_state.board.turn:   
                drawText(screen,"Black Wins by Checkmate!")
            else: 
                drawText(screen,"White Wins by Checkmate!")
        elif game_state.board.is_stalemate():
            game_over = True
            drawText(screen,"Stalemate")
        clock.tick(fps)
        p.display.flip()       
    
def draw_current_board(screen,game_state,squares_selected,play_with_white):
     draw_empty_board(screen)
     highlight_squares(screen,game_state,squares_selected,play_with_white)
     draw_pieces(screen,game_state,play_with_white)
     
def draw_pieces(screen,game_state,play_with_white):
    for color in [ChessEngine.chess.WHITE, ChessEngine.chess.BLACK]:
        for piece in range(1,7):
            if color:
                title = "w" + ChessEngine.chess.piece_symbol(piece).upper()
            else:
                title = "b" + ChessEngine.chess.piece_symbol(piece).upper()
                
            for square in list(game_state.board.pieces(piece,color)):
                c = square % board_dimension
                r = board_dimension - 1 - square // board_dimension
                if not play_with_white:
                    c = 7 - c
                    r = 7 - r
                screen.blit(images[title],p.Rect(c*square_size,r*square_size,square_size,square_size))         
            
def highlight_squares(screen,game_state,squares_selected,play_with_white):
    if squares_selected != ():
        r,c = squares_selected
        start_square = convert_square(squares_selected,play_with_white)
        if game_state.board.color_at(start_square) == game_state.board.turn:
            s = p.Surface((square_size,square_size))
            s.set_alpha(100)
            s.fill(p.Color("blue"))
            screen.blit(s,(c*square_size,r*square_size))
            s.fill(p.Color("yellow"))
            
            for end_square in range(63):
                promote_to = None
                if game_state.board.piece_type_at(start_square) == ChessEngine.chess.PAWN:
                    if (ChessEngine.chess.square_rank(end_square) == 7 or 
                        ChessEngine.chess.square_rank(end_square) == 0):
                        promote_to = ChessEngine.chess.QUEEN
                move = ChessEngine.chess.Move(start_square,end_square,promotion=promote_to)
                if move in game_state.board.legal_moves:
                    square = move.to_square
                    c = square % board_dimension
                    r = board_dimension - 1 - square // board_dimension
                    if not play_with_white:
                        c = 7 - c
                        r = 7 - r
                    screen.blit(s,(c*square_size,r*square_size))    
    
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

def drawText(screen,text):
    font = p.font.SysFont("helvitca",64,True,False)
    textObject = font.render(text,0,p.Color("black"))
    textLocation = p.Rect(0,0,board_width,board_height).move(board_width/2 - textObject.get_width()/2,board_height/2 - textObject.get_height()/2)
    screen.blit(textObject,textLocation)
    textObject = font.render(text,0,p.Color("black"))
    screen.blit(textObject,textLocation.move(2,2))


    
def convert_square(squares_selected,play_with_white):
    if play_with_white:
        return  ((7 - squares_selected[0]) * 8 + 
                        squares_selected[1])
    else:
        return (8 * squares_selected[0] + (7-squares_selected[1]))

if __name__ == "__main__":
    main()




