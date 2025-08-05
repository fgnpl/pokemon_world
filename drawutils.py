import pygame
import constants

# Creating text and attaching it to a specific picture
def drawText(surface, text, pos, font_name="Arial", font_size=15, color=constants.BLACK):
    font = pygame.font.SysFont(font_name, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = pos
    surface.blit(text_surface, text_rect)
