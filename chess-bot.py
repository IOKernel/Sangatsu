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
def startdriver():
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0")
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
    driver.get("https://www.chess.com/live")  

def create_pgn():
    time_now = datetime.now()
    dt_string = time_now.strftime("%d-%m-%Y_%H-%M")
    pgn_loc = script_dir[:-12]+"history/" + dt_string + ".pgn"
    open(pgn_loc, "w+").close
    return pgn_loc

def detect_move(driver, moveNumber):
    colors = [1, 0]
    next_move = ""
    color = colors[moveNumber%2]
    turn = (moveNumber+1)//2
    xpath = f"/html/body/div[3]/div/div[1]/div[1]/div/div[1]/div/div/div[{turn}]/span[{color+2}]/span[contains(@class, 'vertical-move-list-clickable')]"
    WebDriverWait(driver, 120).until(
    EC.presence_of_element_located((By.XPATH, xpath))
    )
    move = driver.find_element_by_xpath(xpath)
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
        return(best_move)

def play_game(driver, engine, auto_start):
    # white move = 0, black move = 1
    if auto_start:
        try:
            time.sleep(1)
            new_match = driver.find_element_by_class_name("game-over-button-button").click()
        except:
            time.sleep(1)
            driver.find_element_by_xpath("//li[@data-tab='challenge']").click()
            driver.find_element_by_class_name("quick-challenge-play").click()
    pgn = create_pgn()
    time.sleep(1)
    try:
        for moveNumber in range(1,500):
            next_move = detect_move(driver, moveNumber)
            with open(pgn, "a") as f:
                f.write(next_move)
            best_move = get_move(engine, pgn)
            highlight_move(driver, best_move)
    except:
        return

def highlight_move(driver, best_move):
    first_square = str(best_move)[:2]
    second_square = str(best_move)[2:]
    first_coord = str(0) + str(ord(first_square[0])-96) + str(0) + first_square[1]
    second_coord = str(0) + str(ord(second_square[0])-96) + str(0) + second_square[1]
    driver.execute_script("""
    element = document.createElement('div');
    element.setAttribute("id", "highlight1");
    style1 = "background-color: rgb(204, 255, 255); opacity: 1;"
    class1 = "square square-{first_coord} marked-square"
    element.setAttribute("style", style1)
    element.setAttribute("class", class1)
    document.getElementById("game-board").appendChild(element)
    element = document.createElement('div');
    element.setAttribute("id", "highlight2");
    style2 = "background-color: rgb(102, 255, 102); opacity: 1;"
    class2 = "square square-{second_coord} marked-square"
    element.setAttribute("style", style2)
    element.setAttribute("class", class2)
    document.getElementById("game-board").appendChild(element)
    """.format(first_coord = first_coord, second_coord = second_coord))


def main():
    driver = startdriver()
    username, password = getCred()
    login(driver, username, password)
    #initialize engine
    engine = chess.engine.SimpleEngine.popen_uci(stockfish_loc)
    play_more = 1
    auto_start = 0
    while play_more:
        play_game(driver, engine, auto_start)
        answer = input("play more? ")
        if answer != 'y':
            play_more = 0
        auto_start = 1
    driver.close()
    engine.close()

if __name__ == "__main__":
    main()