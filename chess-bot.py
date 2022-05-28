import chess
import chess.engine
import chess.pgn
import os
import platform
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#files locations
script_dir = os.path.abspath(__file__)
platform = platform.system()
# checking platform
if platform == 'Linux':
    relative_path = "/Engine/stockfish"
else:
    relative_path = "/Engine/stockfish.exe"
    
stockfish_loc = script_dir[:-13] + relative_path
credentials_loc = script_dir[:-12] + "credentials.txt"

#get account credentials
def getCred():
    with open(credentials_loc, "r") as f:
        username = f.readline().strip()
        password = f.readline().strip()
    if not username and not password:
        print("username/password not provided in credentials.txt")
        username = input("username: ")
        password = input("password: ")
    return [username, password]

#start selenium firefox
def startdriver():
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0")
    if platform == 'Linux':
        gecko_loc = script_dir[:-12] + "geckodriver"
    else:
        gecko_loc = script_dir[:-12] + "geckodriver.exe"
    driver = webdriver.Firefox(profile, executable_path=gecko_loc)
    # login to chess.com
    driver.get("https://www.chess.com/login")
    return driver

def login(driver, username, password):
    usernameBox = driver.find_element_by_id("username")
    usernameBox.send_keys(username)
    passwordBox = driver.find_element_by_id("password")
    passwordBox.send_keys(password)
    passwordBox.send_keys(Keys.RETURN)
    time.sleep(5)
    driver.get("https://www.chess.com/play/online")  

def create_pgn():
    time_now = datetime.now()
    dt_string = time_now.strftime("%d-%m-%Y_%H-%M")
    pgn_loc = script_dir[:-12]+"history/" + dt_string + ".pgn"
    open(pgn_loc, "w+").close
    return pgn_loc

# gets the best move
def get_move(engine, pgn, depth):
    with open(pgn, "r") as f:
        game = chess.pgn.read_game(f)
        board = chess.Board()
        for move in game.mainline_moves():
            board.push(move)
        best_move = engine.play(board, chess.engine.Limit(depth=depth)).move
        return(best_move)


def main():
    driver = startdriver()
    username, password = getCred()
    login(driver, username, password)
    #initialize engine
    engine = chess.engine.SimpleEngine.popen_uci(stockfish_loc)

if __name__ == "__main__":
    main()
    