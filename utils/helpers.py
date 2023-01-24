import os
import time

from utils import downloaders as dl

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import chess

# SCRIPT_DIR is the directory 1 level above this file
SCRIPT_DIR = os.path.dirname(os.path.dirname(__file__))

def get_credentials():
    """
    Check if the credentials file exists and if it does, read it.
    If it doesn't, create it.
    """
    credentials_file = os.path.join(SCRIPT_DIR, 'credentials.txt')
    if os.path.isfile(credentials_file):
        with open(credentials_file, 'r') as f:
            username, password = f.read().splitlines()
    else:
        username = input('Enter your username: ')
        password = input('Enter your password: ')
        with open(credentials_file, 'w') as f:
            f.write(username + '\n' + password)
    return username, password

def get_requirements(OS):
    """
    Validate requirements:
    - check if stockfish is downloaded in bin folder
    - check if geckodriver is downloaded in bin folder
    - check if credentials file exists
    - check if history folder exists
    """
    # check if stockfish is downloaded
    stockfish_path = os.path.join(SCRIPT_DIR, 'bin', 'stockfish')
    if OS == 'Windows':
        stockfish_path += '.exe'
    if not os.path.isfile(stockfish_path):
        # download stockfish
        print('Downloading stockfish...')
        dl.download_stockfish(OS, SCRIPT_DIR)
        print('Done!')
    # check if geckodriver is downloaded
    geckodriver_path = os.path.join(SCRIPT_DIR, 'bin', 'geckodriver')
    if OS == 'Windows':
        geckodriver_path += '.exe'
    if not os.path.isfile(geckodriver_path):
        # download geckodriver
        print('Downloading geckodriver...')
        dl.download_geckodriver(OS, SCRIPT_DIR)
        print('Done!')
    # check if credentials file exists
    username, password = get_credentials()
    history_folder = os.path.join(SCRIPT_DIR, 'history')
    if not os.path.isdir(history_folder):
        print('Creating history folder...')
        os.mkdir(history_folder)
        print('Done!')
    # check if bin folder exists
    bin_folder = os.path.join(SCRIPT_DIR, 'bin')
    if not os.path.isdir(bin_folder):
        print('Creating bin folder...')
        os.mkdir(bin_folder)
        print('Done!')
    return username, password

def start_driver(username, password):
    # create a new Firefox session
    profile = webdriver.FirefoxProfile()
    # profile.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0")
    profile.set_preference("general.useragent.override", "Mozilla/5.0 (X11; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0")
    driver = webdriver.Firefox(profile, executable_path=os.path.join(SCRIPT_DIR, 'bin', 'geckodriver'))
    driver.get('https://www.chess.com/login')
    # login
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
    time.sleep(8)
    driver.get("https://www.chess.com/play/online")
    return driver

def detect_game(driver):
    # or in span class tabs-label with Value: Analysis or Play under div with class tabs-tab and data-tab="game"
    # check the value of the tab using bs4
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    tab_name = soup.find('span', class_='tabs-label')
    if tab_name:
        tab_name = tab_name.text
    else:
        raise Exception('Could not find tabs!')
    if tab_name == 'Analysis':
        return False
    elif tab_name == 'Play':
        return True
    elif tab_name == 'New Game':
        return False
    else:
        raise Exception('Unknown tab name: ' + tab_name)

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