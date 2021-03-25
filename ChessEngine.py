import chess
import random

class GameState():
    def __init__(self,play_with_white: bool):
        self.board = chess.Board()
        
    def make_move(self):
        return random.choice(list(self.board.legal_moves))
        
        