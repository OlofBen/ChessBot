#This is the min max algorithm 
import chess
from chess.engine import PlayResult
import random
from engine_wrapper import EngineWrapper
from strategies import MinimalEngine

class MinMax(MinimalEngine):
    def search(self, board, time_limit, ponder, draw_offered):
        moves = list(board.legal_moves)
        return PlayResult(random.choice(list(board.legal_moves)), None)