import pygame 
import logging 
import json


from .assetManager import AssetManager
from .button import Button
from . import constants as c 
from .tile import Tile 
from .ui_utils import create_text_button_image


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

        # button images
        save_img = AssetManager.get_image("save_btn")
        load_img = AssetManager.get_image("load_btn")
        clear_img = create_text_button_image("CLEAR", 120, 40, (200, 50, 50))

        # Position buttons in the lower margin (below the grid)
        button_y = c.SCREEN_HEIGHT + (c.LOWER_MARGIN // 4) 
        self.save_button = Button(50,  button_y, save_img)
        self.load_button = Button(200, button_y, load_img)
        self.clear_button = Button(350, button_y, clear_img)

        # Create a semi-transparent dark overlay for the whole screen 
        self.overlay = pygame.Surface(
            (
                c.SCREEN_WIDTH + c.SIDE_MARGIN, 
                c.SCREEN_HEIGHT + c.LOWER_MARGIN
            ), 
            pygame.SRCALPHA
        )

        self.overlay.fill((0, 0, 0, 150)) # semi-transparent black

        # Create the popup box image 
        self.confirm_panel = create_text_button_image("CLEAR ALL TILES?", 400, 200, (60, 60, 60))

        # create yes/no buttons 
        yes_img = create_text_button_image("YES", 100, 40, (200, 50, 50))
        no_img  = create_text_button_image("NO", 100, 40, (100, 100, 100))

        # position them in the center of the screen 
        center_x = (c.SCREEN_WIDTH + c.SIDE_MARGIN) // 2 
        center_y = (c.SCREEN_HEIGHT + c.LOWER_MARGIN) // 2 

        self.yes_button = Button(center_x - 110, center_y + 20, yes_img)
        self.no_button = Button(center_x + 10, center_y + 20, no_img)

        self.show_confirm = False   # show overlay state 
        self.input_lockout = False 


    def clear_level(self):
        # re-initialize world_data to all -1 
        self.world_data = [[-1] * c.MAX_COLS for _ in range(c.ROWS)]
        AssetManager.get_sound("dink").play()
        logger.info("Level cleared!")

    def save_level(self):
        try:
            with open("level_data.json", "w") as f:
                json.dump(self.world_data, f) 
            # Play sound on success 
            AssetManager.get_sound("dink").play() 
            logger.info("Level saved!")
        except Exception as e:
            logger.error(f"Save failed: {e}")
    
    def load_level(self):
        try:
            with open("level_data.json", "r") as f:
                self.world_data = json.load(f)
            AssetManager.get_sound("dink").play()
            logger.info("Level loaded!")
        except Exception as e:
            logger.error(f"Load failed: {e}")

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

        
    def draw_buttons(self):
        # draw buttons and check for actions at the same time 
        if self.save_button.draw(self.screen):
            self.save_level() 

        if self.load_button.draw(self.screen):
            self.load_level()

        if self.clear_button.draw(self.screen):
            self.show_confirm = True 
        
    def draw_confirm_popup(self):
        if self.show_confirm:
            # draw dark overlay to focus on the popup
            self.screen.blit(self.overlay, (0,0))

            # draw the main panel box 
            panel_rect = self.confirm_panel.get_rect(
                center=((c.SCREEN_WIDTH + c.SIDE_MARGIN) // 2,
                        (c.SCREEN_HEIGHT + c.LOWER_MARGIN) // 2
                        )
            )

            self.screen.blit(self.confirm_panel, panel_rect)

            # draw yes/no buttons and handle clicks 
            if self.yes_button.draw(self.screen):
                self.clear_level() 
                self.show_confirm = False 
                self.input_lockout = True  # prevent immediate painting

            if self.no_button.draw(self.screen):
                self.show_confirm = False
                self.input_lockout = True # prevent immediate painting when popup disappears

    def draw_mouse_tool_tip(self):
        mx, my = pygame.mouse.get_pos()
        if mx < c.SCREEN_WIDTH and my < c.SCREEN_HEIGHT:
            font = AssetManager.get_font("mario")
            # Show tile number 
            text = font.render(f"Tile: {self.current_tile}", True, (255, 255, 255))

            # draw a small dark background for readability 
            bg_rect = text.get_rect(topleft=(mx+15, my+15))
            pygame.draw.rect(self.screen, (30, 30, 30), bg_rect.inflate(10, 5))
            self.screen.blit(text, bg_rect)

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

        mx, my = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed() 

        if not any(mouse_buttons):
            self.input_lockout = False 

        # Block painting if popup is open
        if not self.show_confirm and not self.input_lockout:
            # Grid Interaction, Continuous Painting
            if mx < c.SCREEN_WIDTH and my < c.SCREEN_HEIGHT:
                column = (mx + self.scroll) // c.TILE_SIZE
                row = my // c.TILE_SIZE 

                if 0 <= row < c.ROWS and 0 <= column < c.MAX_COLS:
                    if mouse_buttons[0]:       # left click to place tile 
                        self.world_data[row][column] = self.current_tile 
                    elif mouse_buttons[2]: # right click to erase 
                        self.world_data[row][column] = -1


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False 

           
            if event.type == pygame.KEYDOWN:
                 # Handle Escape key to close popup
                if event.key == pygame.K_ESCAPE:
                    self.show_confirm = False
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
                # Block sidebar selection if popup is open
                if not self.show_confirm:
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
                

    def run(self):
        while self.running:
            self._handle_events() 

            # Scroll logic 
            if self.scroll_left == True and self.scroll > 0:
                self.scroll -= 5 
            if self.scroll_right == True and self.scroll < c.MAX_SCROLL:
                self.scroll += 5

            # Background and world 
            self.draw_background()
            self.draw_world()
            self.draw_grid()

            # UI panels
            self.draw_side_panel()
            self.draw_mouse_tool_tip()
            self.draw_buttons()    

            # Popup (must be last to be on top)
            self.draw_confirm_popup()

            # update the display 
            pygame.display.flip() 

            # cap the frame rate 
            self.clock.tick(c.FPS)