import chess
import random
import numpy as np
import copy
import time

class GameState():  

    def __init__(self,play_with_white: bool):
        self.board = chess.Board()
        self.DEPTH = 4
        
    def make_move(self):
        global next_move

        think_board = copy.deepcopy(self.board)

        #evaluation = self.find_negamax_move_alpha_beta(think_board,self.DEPTH,-np.inf,np.inf,1 if self.board.turn else -1)

        evaluation,best_move = self.minimax(think_board,self.DEPTH,-np.inf,np.inf,self.board.turn)

        return best_move
        #return random.choice(list(self.board.legal_moves))
        
        
    def find_negamax_move(self,board,depth,multiplier):
        global next_move
        if depth == 0:
            return multiplier * self.static_evaluation(board)
        
        max_score = -np.inf
        legal_moves = list(board.legal_moves)
        for move in legal_moves:
            board.push(move)
            score = -self.find_negamax_move(board,depth-1,-multiplier)
            if score > max_score:
                max_score = score
                if depth == self.DEPTH:
                    next_move = move
            board.pop()
        return max_score
    
    
    def find_negamax_move_alpha_beta(self,board,depth,alpha,beta,multiplier):
        global next_move
        if depth == 0:
            return multiplier * self.static_evaluation(board)
        
        max_score = -np.inf
        legal_moves = list(board.legal_moves)
        for move in legal_moves:
            board.push(move)
            score = -self.find_negamax_move_alpha_beta(board,depth-1,-beta,-alpha,-multiplier)
            if score > max_score:
                max_score = score
                if depth == self.DEPTH:
                    next_move = move
            board.pop()
            if max_score > alpha :
                alpha = max_score
            if alpha >= beta:
                break 
        return max_score
            
        
        
        
        
        
    # For some reason this function is faster than negamax
    def minimax(self,board,depth,alpha,beta,maximizing_player:bool):
        if depth == 0 or board.is_checkmate() or board.is_stalemate() :
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
            
    def static_evaluation(self,board):
        score = 0
        score += self.end_of_game_evaluation(board)
        
        
            
        return score
        
    def end_of_game_evaluation(self,board):
        if board.result() == "1-0":
            score = np.inf
        elif board.result() == "0-1":
            score = -np.inf
        elif board.is_stalemate():
            score = 0
        elif board.is_fivefold_repetition():
            score = 0
            
        return score
        
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


piece_position_evalulation = {
    "P" = [0,0,0,0,0,0,0,0,5,10,10,-20,-20,10,10,5,5,-5,-10,0,0,-10 ,-5,5,0,0,0,20,20,0,0,0,5,5,10,25,25,10,5,5,10,10,20,30,30,20,10,10,50,50,50,50,50,50,50,50,0,0,0,0,0,0,0,0],
    "p" 
    
    
    
    }

