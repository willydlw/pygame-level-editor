# Configuration File Path
ASSETS_CONFIG_PATH = "assets.json"


# Game Window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
LOWER_MARGIN = 100 
SIDE_MARGIN = 300 


FPS = 60            # frames per second


# Grid 
ROWS = 16 
MAX_COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS 

# Limit level width 
MAXIMUM_LEVEL_WIDTH = MAX_COLS * TILE_SIZE
MAX_SCROLL = MAXIMUM_LEVEL_WIDTH - SCREEN_WIDTH


# Sidebar Tiling
SIDEBAR_COLS = 3
SIDEBAR_SLOT_SIZE = 75
SIDEBAR_PADDING = 50
   


# Tile Codes - Background >= 30

TILE_CODE_DICTIONARY = {
    "empty"     : 30,
    "pine1"     : 31,
    "pine2"     : 32,
    "mountain"  : 33,
    "sky_cloud" : 34,
}

