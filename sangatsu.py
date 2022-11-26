import platform
import time

from utils import helpers as hp
from utils import game as gm
# check which OS is running
OS = platform.system()

def main():
    username, password = hp.get_requirements(OS)
    driver = hp.start_driver(username, password)
    engine = gm.start_engine()
    while True:
        game_state = hp.detect_game(driver)
        if game_state:
            # game started
            print('Game started!')
            gm.play_game(driver, engine)
            print('Game ended!, waiting for new game...')
        time.sleep(5)

    
if __name__ == '__main__':
    main()