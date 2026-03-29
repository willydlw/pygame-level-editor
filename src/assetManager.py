import json 
import os
import pygame 
import logging 

from pathlib import Path 


logger = logging.getLogger(__name__)


class NullSound:
    """A fake sound object that does nothing when called."""
    def play(self, *args, **kwargs): return None 
    def stop(self, *args, **kwargs): pass 
    def set_volume(self, *args, **kwargs): pass 
    def get_volume(self): return 0.0 


class AssetManager:
    # Define class-level dictionaries (static variables)
    _images = {}
    _tiles = []         # separate list for index-based access 
    _fonts = {}
    _sounds = {} 

    @classmethod 
    def load_all(cls, config_path):
        logger.info(f"Loading assets, config_path: {config_path}")

        # set up base directory (one level up from where ths script resides)
        # .resolve() gets the absolute path, .parent is the script's folder,
        # and the second .parent goes up one more level 
        BASE_DIR = Path(__file__).resolve().parent.parent 

        # load json configuration file 
        try:
            # join BASE_DIR with the config_path provided 
            full_config_path = BASE_DIR / config_path 
            with open(full_config_path, 'r') as f:
                config = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError, Exception) as e:
            logger.error(f"Failed to load config at {full_config_path}. Error: {e}")
            return 
        
        # Load background and button images
        for name, data in config.get("images", {}).items():
            if isinstance(data, dict):
                path = data.get("path")
                scale = data.get("scale")
            else:
                path = data 
                scale = None 

            is_sky = "sky" in path 

            full_image_path = BASE_DIR / path 
            img = cls._safe_load_image(full_image_path, use_alpha=not is_sky)

            # scale only once, when loading 
            if scale:
                logger.info(f"scaling image {name}, scale: {scale[0]}, {scale[1]}")
                img = pygame.transform.scale(img, (scale[0], scale[1]))

            cls._images[name] = img 

        # Load tile images 
        tile_config = config.get("tiles", {})
        if tile_config:
            folder = Path(tile_config["folder"])
            count = tile_config["count"]
            size = tile_config["scale"]
            
            for i in range(count):
                path = BASE_DIR / folder / f"{i}.png"
                img = cls._safe_load_image(path, True)
                img = pygame.transform.scale(img, size)
                cls._tiles.append(img)

         # Load fonts 
        for name, data in config.get("fonts", {}).items():
            if isinstance(data, dict):
                path = data.get("path", "")
                size = data.get("size", 24)
            else:
                path = data 
                size = 24 

            full_path = BASE_DIR / path 
            cls._fonts[name] = cls._safe_load_font(full_path, size)

        # Load sounds 
        for name, data in config.get("sounds", {}).items():
            if isinstance(data, dict):
                path = data.get("path", "")
            else:
                path = data 

            full_path = BASE_DIR / path
            cls._sounds[name] = cls._safe_load_sound(full_path)


    @staticmethod 
    def _safe_load_image(path, use_alpha=True):
        """Tries to load an image, returns a magenta square on failure"""
        try:
            # .convert_alpha() improves performance for transparent images 
            img = pygame.image.load(str(path))
            return img.convert_alpha() if use_alpha else img.convert() 
        
        except (pygame.error, FileNotFoundError, Exception) as e:
            logger.warning(f"Image missing: {path}")
            # create a 32x32 magenta square as a placeholder 
            fallback = pygame.Surface((32,32))
            fallback.fill((255,0,255))
            return fallback 
        
    
    @staticmethod
    def _safe_load_font(path, size):
        """Tries to load a font; returns system default on failure"""
        try:
            return pygame.font.Font(str(path), size)
        except (pygame.error, FileNotFoundError):
            logger.warning(f"Font missing at {path}. Using system default.")
            return pygame.font.SysFont("Arial", size)
        
    @staticmethod
    def _safe_load_sound(path):
        """Tries to load a sound; returns NullSound on failure"""
        try:
            # Check if mixer is initialized to avoid errors 
            if not pygame.mixer or not pygame.mixer.get_init():
                pygame.mixer_init()
            return pygame.mixer.Sound(str(path))
        except (pygame.error, FileNotFoundError, Exception) as e:
            logger.warning(f"Sound missing at {path}. {e} Using NullSound.")
            return NullSound()
        
    @classmethod
    def get_image(cls, name):
        return cls._images.get(name)
    
    @classmethod 
    def get_tile(cls, index):
        return cls._tiles[index] if 0 <= index < len(cls._tiles) else None
    
    @classmethod
    def get_font(cls, name):
        return cls._fonts.get(name)
    
    @classmethod 
    def get_sound(cls, name):
        """Retrieves a sound; returns NullSound if key doesn't exist"""
        return cls._sounds.get(name, NullSound())
   
    @classmethod
    def __str__(cls):
        summary = [f"AssetManager Status:"]
        summary.append(f"  Images ({len(cls._images)}): {list(cls._images.keys())}")
        summary.append(f"  Fonts  ({len(cls._fonts)}): {list(cls._fonts.keys())}")
        summary.append(f"  Sounds ({len(cls._sounds)}): {list(cls._sounds.keys())}")
        return "\n".join(summary)
