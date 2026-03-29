import pygame 


import logging 

logger = logging.getLogger(__name__)

class Button():
    def __init__(self, x, y, image, scale=False, scaleAmount=1):
        width = image.get_width() 
        height = image.get_height() 
        if scale:
            self.image = pygame.transform.scale(image, (int(width *scaleAmount), int(height * scaleAmount)))
        else:
            self.image = image 
        
        self.rect = self.image.get_rect() 
        self.rect.topleft = (x, y)
        self.clicked = False 

    def draw(self, surface):
        action = False 

        # get mouse position 
        pos = pygame.mouse.get_pos() 

        # check mouseover and clicked conditions 
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True 
                self.clicked = True 

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False 

        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action 