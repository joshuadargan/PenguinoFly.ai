import pygame

from src.Text import Text
from src.State import State


class Menu(State):


    def __init__(self,  window):
        State.__init__(self, State.MENU_STATE, window)
        center_x = self.window.width / 2
        self.title_text_surf, self.title_text_rect = Text.text_objects("Penguino.ai", Text.large_font)
        self.title_text_rect.center = (center_x, (self.window.height / 6))

        self.instructions_text_surf, self.instructions_text_rect = Text.text_objects("Type the letter in () to select an option", Text.tiny_font)
        self.instructions_text_rect.center = (center_x, (self.window.height * 2 / 6))

        self.play_text_surf, self.play_text_rect = Text.text_objects("(P)lay", Text.small_font)
        self.play_text_rect.center = (center_x, (self.window.height * 3 / 6))

        self.ai_text_surf, self.ai_text_rect = Text.text_objects("(A)I Model", Text.small_font)
        self.ai_text_rect.center = (center_x, (self.window.height * 4 / 6))

    def continuous_action(self):
        self.window.screen.blit(self.title_text_surf, self.title_text_rect)
        self.window.screen.blit(self.instructions_text_surf, self.instructions_text_rect)
        self.window.screen.blit(self.play_text_surf, self.play_text_rect)
        self.window.screen.blit(self.ai_text_surf, self.ai_text_rect)
        self.tick_clock(15)

    def keys_pressed_reaction(self):
        if State.is_key_pressed(pygame.K_p):
            # Play the game
            self.state = State.GAME_STATE
            pass
        elif State.is_key_pressed(pygame.K_a):
            # Start ai
            pass