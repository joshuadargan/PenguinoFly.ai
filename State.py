import pygame
pygame.init()

# An interface for different states
class State:

    # Colors
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    light_blue = (200, 255, 255)

    # State types
    MENU_STATE = "Menu"
    GAME_STATE = "Game"
    PAUSE_STATE = "Pause"
    RESTART_STATE = "Restart"

    font_style = 'freesansbold.ttf'
    large_font = pygame.font.Font(font_style, 115)
    small_font = pygame.font.Font(font_style, 75)


    @staticmethod
    def text_objects(text, font):
        textSurface = font.render(text, False, State.black)
        return textSurface, textSurface.get_rect()

    def __init__(self, state_name, window):
        self.state = state_name
        self.window = window
        self.clock = pygame.time.Clock()


    def keys_pressed_reaction(self):
        pass

    def continuous_action(self):
        pass

    # General Method for ticking the clock
    def tick_clock(self, tick_amount):
        self.clock.tick(tick_amount)

    @staticmethod
    def is_key_pressed(key):
        keys = pygame.key.get_pressed()
        return keys[key]
