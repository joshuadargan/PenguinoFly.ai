import pygame
pygame.init()
from src.Color import Color
from src.Window import Window

class Text:
    font_style = pygame.font.get_default_font()
    large_font = pygame.font.Font(font_style, int(Window.height / 6))
    small_font = pygame.font.Font(font_style, int(Window.height / 10))
    tiny_font = pygame.font.Font(font_style, int(Window.height / 20))

    @staticmethod
    def text_objects(text, font):
        textSurface = font.render(text, False, Color.black)
        return textSurface, textSurface.get_rect()
