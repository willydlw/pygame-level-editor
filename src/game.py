import pygame 
import logging 


from .assetManager import AssetManager
from .constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, ASSETS_CONFIG_PATH


# create a logger for this file, named "game" (the filename) 
# Automatically sends its messages up to the Root logger 
# configured in main.py 
logger = logging.getLogger(__name__)

class Game():
    def __init__(self):

        logger.info("Initializing Game object")

        # init pygame modules 
        pygame.init() 

        # set up the window display 
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Level Editor")

        self.clock = pygame.time.Clock()
        self.running = True 

        # Tile group 
        self.tiles = pygame.sprite.Group() 
        logging.info(f"Should self.tiles be a list or a sprite group?")

        # Load assets 
        AssetManager.load_all(ASSETS_CONFIG_PATH)
        logging.info(f"Assets loaded!")

    
    def run(self):
        while self.running:
            # event handling 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False 

            # game logic and drawing code goes here 


            # update the display 
            pygame.display.flip() 

            # cap the frame rate 
            self.clock.tick(FPS)