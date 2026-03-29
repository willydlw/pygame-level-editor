import pygame 
import logging 
from pathlib import Path 

from src import Game


def configure_logger():

    # define absolute path of the log file 
    BASE_DIR = Path(__file__).resolve().parent  # points to directory where main.py resides 

    # / syntax joins a directory and a filename
    # Cross-platform: automatically uses the correct slashes for the 
    # operating system it's running on
    LOG_FILE = BASE_DIR / "editor_errors.log"

    # configure the root logger using the absolute path 
    # all loggers in the project are children of the root and 
    # automatically inherit settings 
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - [%(filename)s: %(lineno)d] - %(message)s',
        handlers=[
            logging.FileHandler(str(LOG_FILE), mode="w"),
            logging.StreamHandler()  # print to console
        ]
    )

    logger = logging.getLogger(__name__)  # create logger for this file 
    logger.info(f"Log file at {LOG_FILE}")


def main():
   
    configure_logger()

    try: 
        game = Game()
        game.run() 
    finally:
        pygame.quit()

    print(f"TODO Ideas: 1. Multiple layers so you can put a tree on top of a grass tile? ")
    print(f"2. Start buidling Game Engine that loads")
    print(f"3. Choose log file save name.")
    print(f"4. Refactor __init__ and other functions for readability?")
    print(f"5. Probably should change class Game to name LevelEditor")


if __name__ == "__main__":
    main()
