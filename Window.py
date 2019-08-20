import pygame
from src.Color import Color


# Holds the settings for the window
class Window:
    height = 700
    width = 1500

    def __init__(self):
        self.keep_open = True
        self.screen = pygame.display.set_mode((Window.width, Window.height))
        Window.width, Window.height = self.screen.get_size()
        print("INFO: screen width - " + str(Window.width) + "  height - " + str(Window.height))

    def fill_base(self):
        self.screen.fill(Color.light_blue)

    def draw(self, entity):
        self.screen.blit(entity.image, entity.get_location())

    def is_open(self):
        return self.keep_open

    def close(self):
        self.keep_open = False

