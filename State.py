import pygame
pygame.init()


# An interface for different states
class State:
    # State types
    MENU_STATE = "Menu"
    GAME_STATE = "Game"
    PAUSE_STATE = "Pause"
    RESTART_STATE = "Restart"
    AI_GAME_STATE = "AI_Game"
    AI_RESTART_STATE = "AI_Restart"

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
