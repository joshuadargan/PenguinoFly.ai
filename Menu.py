import pygame
from src.State import State


class Menu(State):


    def __init__(self,  window):
        State.__init__(self, State.MENU_STATE, window)
        self.title_text_surf, self.title_text_rect = State.text_objects("Penguino.ai", State.large_font)
        self.title_text_rect.center = ((self.window.width / 2), (self.window.height / 6))

    def continuous_action(self):
        self.window.screen.blit(self.title_text_surf, self.title_text_rect)
        self.tick_clock(15)

    def keys_pressed_reaction(self):
        if State.is_key_pressed(pygame.K_p):
            # Play the game
            self.state = State.GAME_STATE
            pass
        elif State.is_key_pressed(pygame.K_a):
            # Start ai
            pass