import chess
import chess.engine
import os
import time
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

def startGame():
    # game is running
    while not board.is_game_over():
        suggestedMove = engine.play(board, chess.engine.Limit(time=0.1))
        print(suggestedMove.move)
        playerMove = input()
        move = chess.Move.from_uci(playerMove)
        board.push(move)
    engine.quit()

def detectMoves(browser):
    # white move = 0, black move = 1
    colors = [1, 0]
    try:
        for moveNumber in range(1,500):
            color = colors[moveNumber%2]
            turn = (moveNumber+1)//2
            print("waiting for the next move")
            xpath = f"/html/body/div[3]/div/div[1]/div[1]/div/div[1]/div/div/div[{turn}]/span[{color+2}]/span[contains(@class, 'vertical-move-list-clickable')]"
            element = WebDriverWait(browser, 120).until(
            EC.presence_of_element_located((By.XPATH, xpath))
            )
            move = browser.find_element_by_xpath(xpath)
            print(moveNumber, move.text)
            # ADD IMPLICIT WAIT
            # DETECT GAME OVER
    except:
        return

def main():
    browser = startBrowser()
    username, password = getCred()
    login(browser, username, password)
    #initialize engine and board
    engine = chess.engine.SimpleEngine.popen_uci(stockfish_loc)
    board = chess.Board()
    detectMoves(browser)
    browser.quit()

main()