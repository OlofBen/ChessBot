"""
Some example strategies for people who want to create a custom, homemade bot.
And some handy classes to extend
"""

from tracemalloc import Statistic
import chess
from chess.engine import PlayResult
import random

from pyparsing import White
from engine_wrapper import EngineWrapper
#from functools import cache


class FillerEngine:
    """
    Not meant to be an actual engine.

    This is only used to provide the property "self.engine"
    in "MinimalEngine" which extends "EngineWrapper"
    """
    def __init__(self, main_engine, name=None):
        self.id = {
            "name": name
        }
        self.name = name
        self.main_engine = main_engine

    def __getattr__(self, method_name):
        main_engine = self.main_engine

        def method(*args, **kwargs):
            nonlocal main_engine
            nonlocal method_name
            return main_engine.notify(method_name, *args, **kwargs)

        return method


class MinimalEngine(EngineWrapper):
    """
    Subclass this to prevent a few random errors

    Even though MinimalEngine extends EngineWrapper,
    you don't have to actually wrap an engine.

    At minimum, just implement `search`,
    however you can also change other methods like
    `notify`, `first_search`, `get_time_control`, etc.
    """
    def __init__(self, commands, options, stderr, draw_or_resign, name=None, **popen_args):
        super().__init__(options, draw_or_resign)

        self.engine_name = self.__class__.__name__ if name is None else name

        self.engine = FillerEngine(self, name=self.name)
        self.engine.id = {
            "name": self.engine_name
        }

    def search(self, board, time_limit, ponder, draw_offered):
        """
        The method to be implemented in your homemade engine

        NOTE: This method must return an instance of "chess.engine.PlayResult"
        """
        raise NotImplementedError("The search method is not implemented")

    def notify(self, method_name, *args, **kwargs):
        """
        The EngineWrapper class sometimes calls methods on "self.engine".
        "self.engine" is a filler property that notifies <self> 
        whenever an attribute is called.

        Nothing happens unless the main engine does something.

        Simply put, the following code is equivalent
        self.engine.<method_name>(<*args>, <**kwargs>)
        self.notify(<method_name>, <*args>, <**kwargs>)
        """
        pass


class ExampleEngine(MinimalEngine):
    pass


# Strategy names and ideas from tom7's excellent eloWorld video

class RandomMove(ExampleEngine):
    def search(self, board, *args):
        return PlayResult(random.choice(list(board.legal_moves)), None)


class Alphabetical(ExampleEngine):
    def search(self, board, *args):
        moves = list(board.legal_moves)
        moves.sort(key=board.san)
        return PlayResult(moves[0], None)


class FirstMove(ExampleEngine):
    """Gets the first move when sorted by uci representation"""
    def search(self, board, *args):
        moves = list(board.legal_moves)
        moves.sort(key=str)
        return PlayResult(moves[0], None)

class MinMax(MinimalEngine):

    def search(self, board, time_limit, ponder, draw_offered):
        print("Thinking")

        def evaluate(board):
            sum = 0
            piece_map = board.piece_map()
            
            for i in piece_map:
                piece = piece_map[i]
                playerFactor = 1 if piece.symbol().isupper() else -1
                symbol = piece.symbol().lower()
                if symbol == 'p': sum += 1*playerFactor
                if symbol == 'q': sum += 9*playerFactor
                if symbol == 'b': sum += 3.25*playerFactor
                if symbol == 'k': sum += 3*playerFactor
                if symbol == 'r': sum += 5*playerFactor
            

                

                
            return sum


        def minMax(board, depth, isWhite):
            """MinMax"""

            if depth == 0 or board.is_game_over():
                return evaluate(board)
            else:
                moves = list(board.legal_moves)
                bestEval = -10000 if isWhite else 10000
                for move in moves:
                    test_board = chess.Board(fen=board.fen())
                    test_board.push(move)
                    eval = minMax(test_board, depth - 1, not isWhite)

                    if isWhite:
                        if eval > bestEval:
                            bestEval = eval
                    else:
                          if eval < bestEval:
                            bestEval = eval
                return bestEval


    
        isWhite = True
        moves = list(board.legal_moves)
        bestEval = -10000 if isWhite else 10000
        bestMove = moves[0]
        for move in moves:
            test_board = chess.Board(fen=board.fen())
            test_board.push(move)
            eval = minMax(test_board, 2, not isWhite)
            if(eval > bestEval):
                bestEval = eval
                bestMove = move
        print(bestEval)
        return PlayResult(bestMove, None)
    
    
