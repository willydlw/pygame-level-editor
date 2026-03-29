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

        # scrolling 
        self.scroll_left = False 
        self.scroll_right = False 
        self.scroll = 0 
        self.scroll_speed = 1

        # tile selection 
        self.current_tile = 0

        # Load assets 
        AssetManager.load_all(c.ASSETS_CONFIG_PATH)
        logging.info(f"Assets loaded!")



    def draw_background(self):
        # clear screen so images don't smear
        self.screen.fill((144, 201, 120)) 

        # define the layers to draw in order (back to front)
        # Sky moves at 0.1x scroll, front pines move at 0.8x scroll 
        # Objects that are closer to use should scroll faster than
        # those farther aways
        layers = ["sky_cloud", "mountain", "pine1", "pine2"]
        multipliers = [0.1, 0.4, 0.6, 0.8]

        for index, name in enumerate(layers):
            img = AssetManager.get_image(name)
            if not img: continue 

            width = img.get_width() 
            layer_scroll = self.scroll * multipliers[index]

            # use modulo on the layer_scroll so this specific layer wraps
            x_offset = layer_scroll % width 

            # draw enough copies to cover the screen width 
            for i in range(6):
                self.screen.blit(img, ((i * width) -x_offset, self._get_layer_y(name, img)))

    def draw_grid(self):
        # vertical lines (scrolling)
        # only need to draw columns that are currently visible on screen
        for col in range(c.MAX_COLS + 1):
            x = col * c.TILE_SIZE - self.scroll 
            if 0 <= x <= c.SCREEN_WIDTH:
                pygame.draw.line(self.screen, (100, 100, 100), (x, 0), (x, c.SCREEN_HEIGHT))

        # horizontal lines (Static)
        for row in range(c.ROWS + 1):
            y = row * c.TILE_SIZE
            pygame.draw.line(self.screen, (100, 100, 100), (0, y), (c.SCREEN_WIDTH, y))


    def draw_side_panel(self):
        # Draw a rectangle on the right side 
        sidebar_rect = pygame.Rect(c.SCREEN_WIDTH, 0, c.SIDE_MARGIN, c.SCREEN_HEIGHT)
        pygame.draw.rect(self.screen, (75,75,75), sidebar_rect)

        # Draw the tiles in the sidebar for selection 
        # Using 3 tiles per row 
        for i in range(len(AssetManager._tiles)):
            tile_img = AssetManager.get_tile(i) 

            x = c.SCREEN_WIDTH + (i % c.SIDEBAR_COLS) * c.SIDEBAR_SLOT_SIZE + c.SIDEBAR_PADDING 
            y = (i // c.SIDEBAR_COLS) * c.SIDEBAR_SLOT_SIZE + c.SIDEBAR_PADDING 

            # Draw a highlight box around the selected tile 
            if self.current_tile == i:
                pygame.draw.rect(self.screen, (255, 255, 0), (x-2, y-2, 36, 36), 2)
            
            self.screen.blit(tile_img, (x, y))



    def _get_layer_y(self, name, img):
        """Helper to get the vertical position for each layer"""
        h = img.get_height() 
        offsets = {
            "sky_cloud": 0,
            "mountain": c.SCREEN_HEIGHT - h - 300,
            "pine1": c.SCREEN_HEIGHT - h - 150,
            "pine2": c.SCREEN_HEIGHT - h
        }

        return offsets.get(name, 0)
       

    
    def run(self):
        while self.running:
            # event handling 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False 

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.scroll_left = True 
                    if event.key == pygame.K_RIGHT:
                        self.scroll_right = True 

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.scroll_left = False 
                    if event.key == pygame.K_RIGHT:
                        self.scroll_right = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # left click 
                        logging.info("Left mouse button pressed")
                        mouse_pos = pygame.mouse.get_pos() 

                        # check if the click is inside the sidebar 
                        if mouse_pos[0] > c.SCREEN_WIDTH:
                            # Calculate which tile index was clicked based
                            # on the grid math 
                            col = (mouse_pos[0] - c.SCREEN_WIDTH - c.SIDEBAR_PADDING) // c.SIDEBAR_SLOT_SIZE 
                            row = (mouse_pos[1] - c.SIDEBAR_PADDING) // c.SIDEBAR_SLOT_SIZE 
                            index = col + row * c.SIDEBAR_COLS

                            if 0 <= index < len(AssetManager._tiles):
                                self.current_tile = index 


            # limit scrolling to left to not go beyond x = 0 
            if self.scroll_left == True and self.scroll > 0:
                self.scroll -= 5 
            if self.scroll_right == True and self.scroll < c.MAX_SCROLL:
                self.scroll += 5

            # draw the scrolling background
            self.draw_background()
            self.draw_grid()
            self.draw_side_panel()

            # update the display 
            pygame.display.flip() 

            # cap the frame rate 
            self.clock.tick(c.FPS)