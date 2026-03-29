# Configuration File Path
ASSETS_CONFIG_PATH = "assets.json"

# Assets Tile Size 
TILE_SIZE = 32 

# Define rows and columns we want in the grid
ROWS = 20
COLS_VISIBLE = 25
MAX_COLS = 150


# Calculate screen height and width to fit
SCREEN_WIDTH = COLS_VISIBLE * TILE_SIZE  # 25 * 32 = 800
SCREEN_HEIGHT = ROWS * TILE_SIZE         # 20 * 32 = 640

# Margins for user interface
SIDE_MARGIN = 300
LOWER_MARGIN = 100 


# Frames per second
FPS = 60         


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

