import pygame 
import logging 


from .assetManager import AssetManager
from . import constants as c 
from .tile import Tile 


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
        self.screen = pygame.display.set_mode(
            (c.SCREEN_WIDTH + c.SIDE_MARGIN, c.SCREEN_HEIGHT + c.LOWER_MARGIN))
        pygame.display.set_caption("Level Editor")

        self.clock = pygame.time.Clock()
        self.running = True 

        # Tile group 
        self.background_tiles = pygame.sprite.Group() 
        logging.info(f"Should self.tiles be a list or a sprite group?")

        # Load assets 
        AssetManager.load_all(c.ASSETS_CONFIG_PATH)
        logging.info(f"Assets loaded!")

        # Initialize background 
        self.setup_background()


    def setup_background(self):
        sky_tile = Tile(0, 0, AssetManager.get_image("sky_cloud"), c.TILE_CODE_DICTIONARY.get("sky_cloud"))
        self.background_tiles.add(sky_tile)

        mountain_img = AssetManager.get_image("mountain")

        if mountain_img: 
            m_height = mountain_img.get_height() 
            mountain_tile = Tile(0, c.SCREEN_HEIGHT - m_height - 300, mountain_img, c.TILE_CODE_DICTIONARY.get("mountain"))
            self.background_tiles.add(mountain_tile)
        
        pine1_img = AssetManager.get_image("pine1")
        if pine1_img:
            pine1_height = pine1_img.get_height() 
            pine1_tile = Tile(0, c.SCREEN_HEIGHT - pine1_height - 150, pine1_img, c.TILE_CODE_DICTIONARY.get("pine1"))
            self.background_tiles.add(pine1_tile)
        
        pine2_img = AssetManager.get_image("pine2")
        if pine2_img:
            pine2_height = pine2_img.get_height() 
            pine2_tile = Tile(0, c.SCREEN_HEIGHT - pine2_height, pine2_img, c.TILE_CODE_DICTIONARY.get("pine2"))
            self.background_tiles.add(pine2_tile)

    
    def run(self):
        while self.running:
            # event handling 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False 

            # game logic and drawing code goes here 
            self.background_tiles.draw(self.screen)


            # update the display 
            pygame.display.flip() 

            # cap the frame rate 
            self.clock.tick(c.FPS)