import os
import platform
import time
import chess
import chess.engine
import chess.pgn
from configparser import ConfigParser
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# files locations
script_dir = os.path.abspath(__file__)
platform = platform.system()
# checking platform
if platform == 'Linux':
    relative_path = "/Engine/stockfish"
else:
    relative_path = "/Engine/stockfish.exe"
    
stockfish_loc = script_dir[:-13] + relative_path
credentials_loc = script_dir[:-12] + "credentials.txt"


# get username and password from credentials.txt, if it doesn't exist, ask user for it
def get_credentials():
    if os.path.isfile(credentials_loc):
        with open(credentials_loc, 'r') as f:
            credentials = f.read().splitlines()
        return credentials
    else:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        with open(credentials_loc, 'w') as f:
            f.write(username + "\n" + password)
        return [username, password]

# start webdriver using geckodriver
def startdriver():
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0")
    if platform == 'Linux':
        gecko_loc = script_dir[:-12] + "geckodriver"
    else:
        gecko_loc = script_dir[:-12] + "geckodriver.exe"
    driver = webdriver.Firefox(profile, executable_path=gecko_loc)
    # open logic page
    driver.get("https://www.chess.com/login")
    return driver

# login to chess.com with username password using selenium
def login(driver, username, password):
    # wait for username field to be visible
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    # enter username
    username_field.send_keys(username)
    # wait for password field to be visible
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "password"))
    )
    # enter password and login
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    time.sleep(5)
    driver.get("https://www.chess.com/play/online")

# play game function, input is the driver, the game engine
def play_game(driver, engine):
    board = chess.Board()
    for moveNum in range(1,200):
        try:
            result = driver.find_element_by_class_name("white node game-result").text
            print(result)
            return "game over"
        except:
            move = detect_move(driver, moveNum)
            remove_highlight(driver)
            if move[0].isdigit():
                result = driver.find_element_by_class_name("game-result").text
                print(result)
                return "game over"
            best_move = get_best_move(engine, board, move)
            highlight_move(driver, best_move)

# function to get best move from engine, input is engine, board and move
def get_best_move(engine, board, move):
    # make move on board
    board.push_san(move)
    # get best move from engine
    best_move = engine.play(board, chess.engine.Limit(depth=13))
    # get move from engine
    move = best_move.move
    return move

# detect move in html xpath
def detect_move(driver, moveNum):
    # wait for move to be visible or for game to be over in a while loop
    while True:
        try:
            move = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.XPATH, f"//div[@data-ply='{moveNum}']"))
            )
            return move.text
        except:
            try:
                result = driver.find_element_by_class_name("game-result").text
                return result
            except:
                pass

def highlight_move(driver, best_move):
    first_square = str(best_move)[:2]
    second_square = str(best_move)[2:]
    first_coord = str(ord(first_square[0])-96) + first_square[1]
    second_coord = str(ord(second_square[0])-96) + second_square[1]
    driver.execute_script(f"""
    element = document.createElement('div');
    element.setAttribute("class", "highlight square-{first_coord}");
    style1 = "background-color: rgb(204, 255, 255); opacity: 0.6;"
    element.setAttribute("style", style1)
    document.getElementsByClassName("board")[0].appendChild(element)
    element = document.createElement('div');
    style2 = "background-color: rgb(102, 205, 102); opacity: 0.6;"
    element.setAttribute("style", style2)
    element.setAttribute("class", "highlight square-{second_coord}");
    document.getElementsByClassName("board")[0].appendChild(element)
    """)

# function to remove a div with class highlight
def remove_highlight(driver):
    driver.execute_script("""
    var elements = document.getElementsByClassName("highlight");
    while (elements.length > 0) {
        elements[0].parentNode.removeChild(elements[0]);
    }
    """)

def main():
    # initialize webdriver, game engine and login
    driver = startdriver()
    username, password = get_credentials()
    login(driver, username, password)
    engine = chess.engine.SimpleEngine.popen_uci(stockfish_loc)
    
    while True:
        # ask user if ready to play, if not, exit
        ready = input("Are you ready to play? (y/n): ")
        if ready == 'n':
            print("Goodbye!")
            driver.close()
            engine.close()
            return
        # play game
        play_game(driver, engine)


if __name__ == "__main__":
    main()