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

        # create a 2D list to save the tilemap data 
        self.world_data = [] 
        for row in range(c.ROWS):
            r = [-1] * c.MAX_COLS 
            self.world_data.append(r)

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
        # Draw the sidebar rectangle to right of game sreen 
        sidebar_rect = pygame.Rect(c.SCREEN_WIDTH, 0, c.SIDE_MARGIN, c.SCREEN_HEIGHT)
        pygame.draw.rect(self.screen, (75,75,75), sidebar_rect)

        # Draw the tiles in the sidebar for selection 
        # Using 3 tiles per row 
        for i in range(len(AssetManager._tiles)):
            tile_img = AssetManager.get_tile(i) 

            x = c.SCREEN_WIDTH + (i % c.SIDEBAR_COLS) * c.SIDEBAR_SLOT_SIZE + c.SIDEBAR_PADDING 
            y = (i // c.SIDEBAR_COLS) * c.SIDEBAR_SLOT_SIZE + c.SIDEBAR_PADDING 

            # hover effect when mouse if over a tile
            tile_rect = pygame.Rect(x, y, c.TILE_SIZE, c.TILE_SIZE)
            # grow the rect by 2 pixels on each side to see the hover rect
            hover_rect = tile_rect.inflate(4,4)
            mouse_pos = pygame.mouse.get_pos()

            # draw the hover effect
            if tile_rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, (200, 200, 200), hover_rect, 2)

            # Draw the selection effect 
            if self.current_tile == i:
                pygame.draw.rect(self.screen, (255, 255, 0), (x-2, y-2, 36, 36), 3)
            
            self.screen.blit(tile_img, (x, y))


    def draw_world(self):
        for y, row in enumerate(self.world_data):
            for x, tile_index in enumerate(row):
                if tile_index != -1:
                    img = AssetManager.get_tile(tile_index)
                    # subtract scroll so the tiles move when you scroll 
                    self.screen.blit(img, (x * c.TILE_SIZE - self.scroll, y * c.TILE_SIZE))


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
       

    def _handle_events(self):
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
                mx, my = pygame.mouse.get_pos() 

                # Sidebar Selection 
                if mx > c.SCREEN_WIDTH:
                    # left click selects tile
                    if event.button == 1:
                        col = (mx - c.SCREEN_WIDTH - c.SIDEBAR_PADDING) // c.SIDEBAR_SLOT_SIZE
                        row = (my - c.SIDEBAR_PADDING) // c.SIDEBAR_SLOT_SIZE 
                        index = col + (row * c.SIDEBAR_COLS) 

                        if 0 <= index < len(AssetManager._tiles):
                            # calculate the EXACT 32x32 area for that specific tile to 
                            # avoid a ghost index for selecting padded area 
                            tile_x = c.SCREEN_WIDTH + (col * c.SIDEBAR_SLOT_SIZE) + c.SIDEBAR_PADDING
                            tile_y = (row * c.SIDEBAR_SLOT_SIZE) + c.SIDEBAR_PADDING 
                            
                            # create a temporary rectangle 
                            tile_rect = pygame.Rect(tile_x, tile_y, c.TILE_SIZE, c.TILE_SIZE)

                            # only select if mouse is inside that tile rect area 
                            if tile_rect.collidepoint(mx, my):
                                self.current_tile = index 
                                logging.info(f"Selected tile index: {index}")
                
                # Grid Interaction 
                elif mx < c.SCREEN_WIDTH and my < c.SCREEN_HEIGHT:
                    column = (mx + self.scroll) // c.TILE_SIZE
                    row = my // c.TILE_SIZE 

                    if 0 <= row < c.ROWS and 0 <= column < c.MAX_COLS:
                        if event.button == 1:       # left click to place tile 
                            self.world_data[row][column] = self.current_tile 
                        elif event.button == 3: # right click to erase 
                            self.world_data[row][column] = -1


    def run(self):
        while self.running:
            self._handle_events() 

            # limit scrolling to left to not go beyond x = 0 
            if self.scroll_left == True and self.scroll > 0:
                self.scroll -= 5 
            if self.scroll_right == True and self.scroll < c.MAX_SCROLL:
                self.scroll += 5

            # draw the scrolling background
            self.draw_background()
            self.draw_world()
            self.draw_grid()
            self.draw_side_panel()

            # update the display 
            pygame.display.flip() 

            # cap the frame rate 
            self.clock.tick(c.FPS)