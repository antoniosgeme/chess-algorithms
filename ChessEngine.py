import chess
import random
import numpy as np
import copy

class GameState():  

    def __init__(self,play_with_white: bool):
        self.board = chess.Board()
        
    def make_move(self):
        think_board = copy.deepcopy(self.board)
        
        evaluation,best_move = self.minimax(think_board,4,-np.inf,np.inf,self.board.turn)
        return best_move
        #return random.choice(list(self.board.legal_moves))
        
    def minimax(self,board,depth,alpha,beta,maximizing_player:bool):
        if depth == 0 or board.is_checkmate() or board.is_checkmate() :
            return self.material_evaluation(board),None
        if maximizing_player:
            max_eval = -np.inf
            legal_moves = list(board.legal_moves)
            best_move = legal_moves[0]
            for move in legal_moves:
                board.push(move)
                evaluation,empty_move = self.minimax(board,depth-1,alpha,beta,False)
                if evaluation > max_eval:
                    max_eval = evaluation
                    best_move = move
                board.pop()
                alpha = max(alpha,evaluation)
                if beta <= alpha:
                    break
            return max_eval,best_move
        else:
            min_eval = np.inf
            legal_moves = list(board.legal_moves)
            best_move = legal_moves[0]
            for move in legal_moves:
                board.push(move)
                evaluation,empty_move = self.minimax(board,depth-1,alpha,beta,True)
                if evaluation < min_eval:
                    min_eval = evaluation
                    best_move = move
                board.pop()
                beta = min(beta,evaluation)
                if beta <= alpha:
                    break
            return min_eval,best_move
            
        
    
    def material_evaluation(self,board):
        """
        Adds the material on the board. White pieces are positive, black are negative
        """
        score = 0
        for piece in board.board_fen():
            score += fen_dict[piece]
        return score
            
fen_dict = {"r":-500,
            "R":500,
            "n":-300,
            "N":300,
            "b":-300,
            "B":300,
            "q":-900,
            "Q":900,
            "k":0,
            "K":0,
            "p":-100,
            "P":100,
            "/":0,
            "1":0,
            "2":0,
            "3":0,
            "4":0,
            "5":0,
            "6":0,
            "7":0,
            "8":0}