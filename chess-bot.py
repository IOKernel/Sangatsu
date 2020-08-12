import chess
import chess.engine
import os
import sys

#I hate windows/linux pathing
script_dir = os.path.abspath(__file__)
relative_path = "/Engine/stockfish.exe"
stockfish_loc = script_dir[:-13] + relative_path
#Stockfish location
engine = chess.engine.SimpleEngine.popen_uci(stockfish_loc)
board = chess.Board()
# game is running
while not board.is_game_over():
    result = engine.play(board, chess.engine.Limit(time=0.1))
    print(result.move)
    playerMove = input()
    move = chess.Move.from_uci(playerMove)
    board.push(move)
engine.quit()