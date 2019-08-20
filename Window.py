import pygame
from src.Icicle import Ice
from pygame import Color
from pygame import locals
from pygame import display
from src.State import State


# Holds the settings for the window
class Window:
    height = 0
    width = 0

    def __init__(self):
        self.keep_open = True
        self.screen = pygame.display.set_mode((1500,700))
        Window.width, Window.height = self.screen.get_size()
        print("INFO: screen width - " + str(Window.width) + "  height - " + str(Window.height))

    def fill_base(self):
        self.screen.fill(State.light_blue)

    def draw(self, entity):
        self.screen.blit(entity.image, entity.get_location())

    def is_open(self):
        return self.keep_open

    def close(self):
        self.keep_open = False

