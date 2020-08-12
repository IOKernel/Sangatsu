import chess
import chess.engine
import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

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

def startGame():
    # game is running
    while not board.is_game_over():
        suggestedMove = engine.play(board, chess.engine.Limit(time=0.1))
        print(suggestedMove.move)
        playerMove = input()
        move = chess.Move.from_uci(playerMove)
        board.push(move)
    engine.quit()



def main():
    browser = startBrowser()
    username, password = getCred()
    login(browser, username, password)
    #initialize engine and board
    engine = chess.engine.SimpleEngine.popen_uci(stockfish_loc)
    board = chess.Board()
    engine.quit()


main()