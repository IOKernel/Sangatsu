import chess
import chess.engine
import chess.pgn
import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#files locations
script_dir = os.path.abspath(__file__)
relative_path = "/Engine/stockfish.exe"
stockfish_loc = script_dir[:-13] + relative_path
credentials_loc = script_dir[:-12] + "credentials.txt"

#get account credentials
def getCred():
    with open(credentials_loc, "r") as f:
        username = f.readline().strip()
        password = f.readline().strip()
    return [username, password]

#start selenium firefox
def startBrowser():
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0")
    gecko_loc = script_dir[:-12] + "geckodriver.exe"
    browser = webdriver.Firefox(profile, executable_path=gecko_loc)
    # login to chess.com
    browser.get("https://www.chess.com/login")
    return browser

def login(browser, username, password):
    usernameBox = browser.find_element_by_id("username")
    usernameBox.send_keys(username)
    passwordBox = browser.find_element_by_id("password")
    passwordBox.send_keys(password)
    passwordBox.send_keys(Keys.RETURN)
    time.sleep(5)
    browser.get("https://www.chess.com/live")  

def create_pgn():
    time_now = datetime.now()
    dt_string = time_now.strftime("%d-%m-%Y_%H-%M")
    pgn_loc = script_dir[:-12]+"history/" + dt_string + ".pgn"
    print(pgn_loc)
    open(pgn_loc, "w+").close
    return pgn_loc

def detect_move(browser, moveNumber):
    colors = [1, 0]
    next_move = ""
    color = colors[moveNumber%2]
    turn = (moveNumber+1)//2
    xpath = f"/html/body/div[3]/div/div[1]/div[1]/div/div[1]/div/div/div[{turn}]/span[{color+2}]/span[contains(@class, 'vertical-move-list-clickable')]"
    WebDriverWait(browser, 120).until(
    EC.presence_of_element_located((By.XPATH, xpath))
    )
    move = browser.find_element_by_xpath(xpath)
    print(moveNumber, move.text)
    # Check if game is over
    if move.text[0].isdigit():
        print("GAME OVER")
        return #GAME OVER
    if moveNumber % 2 == 1:
        return str(turn) + "." + move.text + " "
    else:
        return move.text + " "

def get_move(engine, pgn):
    with open(pgn, "r") as f:
        game = chess.pgn.read_game(f)
        board = chess.Board()
        for move in game.mainline_moves():
            board.push(move)
        best_move = engine.play(board, chess.engine.Limit(depth=14)).move 
        print(best_move)
            


def play_game(browser, engine):
    # white move = 0, black move = 1
    pgn = create_pgn()
    try:
        for moveNumber in range(1,500):
            next_move = detect_move(browser, moveNumber)
            with open(pgn, "a") as f:
                f.write(next_move)
            get_move(engine, pgn)
    except:
        return

def main():
    browser = startBrowser()
    username, password = getCred()
    login(browser, username, password)
    #initialize engine and board
    engine = chess.engine.SimpleEngine.popen_uci(stockfish_loc)
    play_game(browser, engine,)
    browser.close()

main()