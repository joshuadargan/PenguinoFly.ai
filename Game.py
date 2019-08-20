import pygame
from src.State import State
from src.Icicle import IceBoundary, Icicle, Ice
from src.Penguin import Penguin
from src.Window import Window


class Game:
    spacing = 150
    start_count = 51

    # Sub-states
    PAUSE_STATE = "Pause"
    DEAD_STATE = "Dead"

    def __init__(self, window):
        State.__init__(self, State.GAME_STATE, window)
        self.substate = State.GAME_STATE
        self.penguin = Penguin(window.width / 3, window.height / 2)
        self.entities = []
        ice_boundary = IceBoundary(window.width, window.height)
        self.entities = self.entities + ice_boundary.floor + ice_boundary.ceiling
        self.game_count = 0
        self.score = 0

        self.score_text_surf, self.score_text_rect = State.text_objects(str(self.score), State.small_font)
        self.score_text_rect.center = ((self.window.width * 4 / 5), (self.window.height / 6))

    def update_score(self):
        self.score_text_surf, self.score_text_rect = State.text_objects(str(self.score), State.small_font)
        self.score_text_rect.center = ((self.window.width * 4 / 5), (self.window.height / 6))

    def continuous_action(self):
        if self.substate == State.GAME_STATE:
            if self.game_count > Game.start_count:
                if self.game_count % Game.spacing == 0:
                    icicle = Icicle(self.window.width, self.window.height)
                    # Add the icicle to the entities list
                    self.entities.append(icicle)
                self.penguin.move()
            for entity in self.entities:
                # if off screen
                if entity.get_location()[0] < Icicle.neg_gap_size:
                    if entity.name == Ice.icicle_type:
                        self.entities.remove(entity)
                        print("UPDATE: Removed entity")
                    elif entity.name == Ice.floor_type or entity.name == Ice.ceiling_type:
                        entity.set_x(self.window.width)
                else:
                    entity.move()
                    if entity.name == Icicle.name:
                        if not entity.is_counted() and entity.x + self.penguin.get_width() < self.penguin.x:
                            entity.scored()
                            self.score += 1
                            self.update_score()

                        for subentity in entity.get_entity():
                            self.window.draw(subentity)
                            if self.penguin.is_collided_with(subentity):
                                self.substate = Game.DEAD_STATE
                                print("Penguin collided with " + entity.name)
                    else:
                        self.window.draw(entity)
                        if self.penguin.is_collided_with(entity):
                            self.substate = Game.DEAD_STATE
            self.game_count += 1
        elif self.substate == Game.DEAD_STATE or self.substate == Game.PAUSE_STATE:
            # Draw the background
            for entity in self.entities:
                if entity.name == Icicle.name:
                    for subentity in entity.get_entity():
                        self.window.draw(subentity)
                else:
                    self.window.draw(entity)
            if self.substate == Game.DEAD_STATE:
                pass
            elif self.substate == Game.PAUSE_STATE:
                pass
        self.window.draw(self.penguin)
        self.window.screen.blit(self.score_text_surf, self.score_text_rect)

    def keys_pressed_reaction(self):
        if self.substate == State.GAME_STATE:
            if State.is_key_pressed(pygame.K_SPACE) and self.game_count > Game.start_count:
                self.penguin.flapped()
            elif State.is_key_pressed(pygame.K_p):
                # Pause the game
                self.substate = Game.PAUSE_STATE
        elif self.substate == Game.PAUSE_STATE:
            if State.is_key_pressed(pygame.K_u):
                self.substate = State.GAME_STATE
            elif State.is_key_pressed(pygame.K_q):
                self.state = State.MENU_STATE
        elif self.substate == Game.DEAD_STATE:
            if State.is_key_pressed(pygame.K_SPACE):
                self.state = State.RESTART_STATE
            elif State.is_key_pressed(pygame.K_m):
                self.state = State.MENU_STATE
