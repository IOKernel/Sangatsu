import os
import datetime

import chess
import chess.engine
import chess.pgn

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils import helpers as hp

SCRIPT_DIR = os.path.dirname(os.path.dirname(__file__))
DEPTH = 17

def get_top_moves(board, engine, depth, num_moves):
    info = engine.analyse(board, chess.engine.Limit(depth=depth))
    moves = []
    try:
        length = min(num_moves, len(info['pv']))
        for i in range(length):
            moves.append(info['pv'][i])
        return moves
    except KeyError:
        print(info)
        print('No moves found')
        return []

def start_engine():
    engine = chess.engine.SimpleEngine.popen_uci(os.path.join(SCRIPT_DIR, 'bin', 'stockfish'))
    return engine

def detect_move(driver, move_number:int , turn: bool, bot_game = False, timeout=360):
    # wait for either the move or the game to end
    # xpath = //move-list-wrapper/vertical-move-list/div[3]/div[1]
    if bot_game:
        turn_val = 1 if turn else 2
    else:
        turn_val = 1 if turn else 3
    # move = WebDriverWait(driver, timeout).until(
    #     EC.presence_of_element_located((By.XPATH, f'//vertical-move-list/div[{move_number}]/div[{turn_val}]')))
    # loop in 5 second intervals over timeout period to check for div[move_number]/div[turn_val] or div[move_number]/span
    # if div[move_number]/span is found, game has ended
    # if div[move_number]/div[turn_val] is found, move has been made

    for i in range(timeout//5):
        try:
            move = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, f'//vertical-move-list/div[{move_number}]/div[{turn_val}]')))
            break
        except:
            try:
                # check without waiting
                move = driver.find_element_by_xpath(f'//vertical-move-list/div[{move_number}]/span')
                break
            except:
                pass
    return move.text

def play_game(driver, engine):
    board = chess.Board()
    is_bot_game = hp.detect_bot_game(driver)
    while True:
        turn = board.turn
        move_number = board.fullmove_number
        move = detect_move(driver, move_number, turn, bot_game=is_bot_game)
        print(move)
        hp.remove_highlight(driver)
        if move[0].isdigit():
            print("Game ended!")
            save_game(board, move)
            return move
        # check if move is valid
        board.push_san(move)
        if board.is_checkmate():
            save_game(board, board.result())
            print("Game ended!")
            return move
        moves = get_top_moves(board, engine, DEPTH, 3)
        # for move in moves:
        #     hp.highlight_move(driver, move)
        hp.highlight_move(driver, moves[0])

def save_game(board, result = ''):
    HISTORY_DIR = os.path.join(SCRIPT_DIR, 'history')
    game = chess.pgn.Game()
    game.headers['Event'] = 'Sangatsu'
    game.headers['Site'] = 'https://www.chess.com/'
    game.headers['Date'] = str(datetime.date.today())
    game.headers['Round'] = '1'
    if result:
        game.headers['Result'] = result
    else:
        game.headers['Result'] = board.result()
    node = game.add_variation(board.move_stack[0])
    for move in board.move_stack[1:]:
        node = node.add_variation(move)
    # add time to filename
    filename = f'{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")}.pgn'
    with open(os.path.join(HISTORY_DIR, filename), 'w') as f:
        f.write(game.accept(chess.pgn.StringExporter()))