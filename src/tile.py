import pygame 
import logging 



logger = logging.getLogger(__name__)


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, image, code):
        super().__init__() 
        self.image = image 
        self.rect = self.image.get_rect(topleft=(x,y))
        self.hitbox = self.rect 
        self.code = code 

    def __str__(self):
        return f"Tile at ({self.rect.x}, {self.rect.y}), code: {self.code}"