import pygame 

import logging 

from .assetManager import AssetManager

logger = logging.getLogger(__name__)

def create_text_button_image(text, width, height, color, font_name="mario"):
    # create a transparent surface 
    surf = pygame.Surface((width, height), pygame.SRCALPHA)

    # draw a rounded rectangle for the background 
    pygame.draw.rect(surf, color, (0, 0, width, height), border_radius=5)

    # add a white border for better visibility 
    pygame.draw.rect(surf, (255,255,255), (0, 0, width, height), 2, border_radius=5)

    # render the text 
    font = AssetManager.get_font(font_name)
    text_surf = font.render(text, True, (255, 255, 255))

    # center the text 
    text_rect = text_surf.get_rect(center=(width//2, height//2))
    surf.blit(text_surf, text_rect)

    return surf 