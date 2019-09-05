import pygame

from src.Text import Text
from src.State import State
from src.Icicle import IceBoundary, Icicle, Ice
from src.Penguin import Penguin
from src.Window import Window
from src.NeuralNetwork import Brain
from src.NeuralNetwork import BrainControl

class Game:
    spacing = 150

    # Sub-states
    PAUSE_STATE = "Pause"
    DEAD_STATE = "Dead"
    AI_DEAD_STATE = "AI_Dead"

    def __init__(self, window, state=State.GAME_STATE):
        State.__init__(self, state, window)
        self.substate = state
        self.penguin = Penguin(window.width / 3, window.height / 2)
        self.entities = []
        ice_boundary = IceBoundary(window.width, window.height)
        self.entities = self.entities + ice_boundary.floor + ice_boundary.ceiling
        self.game_count = 0

        # AI needs this info
        self.closest_gap_range = (0,window.height)
        self.closest_x_distance_to_penguin = window.width - self.penguin.x
        self.old_state = None
        self.environment_state = None
        self.reward = 0

        # Score message
        self.score = 0
        self.score_text_surf, self.score_text_rect = Text.text_objects(str(self.score), Text.small_font)
        self.score_text_rect.center = ((self.window.width * 4 / 5), (self.window.height / 6))

        # Game start screen
        self.game_started = False
        self.spacebar_text_surf, self.spacebar_text_rect = Text.text_objects("To begin and to flap, hit the (Spacebar)", Text.tiny_font)
        self.spacebar_text_rect.center = ((self.window.width / 2), (self.window.height / 3))

        self.p_to_pause_text_surf, self.p_to_pause_text_rect = Text.text_objects("(P) to pause", Text.tiny_font)
        self.p_to_pause_text_rect.center = ((self.window.width / 2), (self.window.height * 2 / 3))

        # Quit text
        self.quit_text_surf , self.quit_text_rect = Text.text_objects("(Q)uit to menu", Text.tiny_font)
        self.quit_text_rect.center = ((self.window.width / 2), (self.window.height * 2 / 3))

        # Unpause text
        self.unpause_text_surf, self.unpause_text_rect = Text.text_objects("(U)npause", Text.small_font)
        self.unpause_text_rect.center = ((self.window.width / 2), (self.window.height / 3))

        # Restart text
        self.restart_text_surf, self.restart_text_rect = Text.text_objects("(P)lay Again", Text.small_font)
        self.restart_text_rect.center = ((self.window.width / 2), (self.window.height / 3))

        self.update_score()

        if self.substate == State.AI_GAME_STATE:
            self.game_started = True



    def update_score(self):
        self.score_text_surf, self.score_text_rect = Text.text_objects(str(self.score), Text.small_font)
        self.score_text_rect.center = ((self.window.width * 4 / 5), (self.window.height / 6))

    def continuous_action(self):
        if (self.substate == State.GAME_STATE and self.game_started) or self.substate == State.AI_GAME_STATE:

            if self.game_count % Game.spacing == 0:
                icicle = Icicle(self.window.width, self.window.height)
                # Add a new icicle to the entities list
                self.entities.append(icicle)

            # Move all entities and check for scoring and collisions
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
                        # Player scored?
                        if not entity.is_counted() and entity.x + self.penguin.get_width() < self.penguin.x:
                            entity.scored()
                            self.score += 1
                            self.update_score()
                            self.reward = 1

                        for subentity in entity.get_entity():
                            if self.penguin.is_collided_with(subentity):
                                if self.substate == State.AI_GAME_STATE:
                                    self.substate = Game.AI_DEAD_STATE
                                    self.reward = -10
                                elif self.substate == State.GAME_STATE:
                                    self.substate = Game.DEAD_STATE

                                print("Penguin collided with " + entity.name)
                    else:
                        if self.penguin.is_collided_with(entity):
                            if self.substate == State.AI_GAME_STATE:
                                self.substate = Game.AI_DEAD_STATE
                                self.reward = -10
                            elif self.substate == State.GAME_STATE:
                                self.substate = Game.DEAD_STATE

            self.game_count += 1

        # if the closest icicle is about to pass the bird, reset the closest x distance
        if self.closest_x_distance_to_penguin <= Ice.x_vel:
            self.closest_x_distance_to_penguin = Game.spacing * 2

        # Draw the entities
        for entity in self.entities:
            if entity.name == Icicle.name:

                # if in front of penguin and less than the previous closest distance to the penguin
                if entity.x > self.penguin.x and self.closest_x_distance_to_penguin > entity.x - self.penguin.x:
                    # set the new closest to x value and gap values
                    self.closest_x_distance_to_penguin = entity.x - self.penguin.x
                    self.closest_gap_range = entity.gap_range
                    print("Closest to penguin x: " + str(self.closest_x_distance_to_penguin) + " gap_range: " + str(self.closest_gap_range))


                for subentity in entity.get_entity():
                    self.window.draw(subentity)
            else:
                self.window.draw(entity)
        self.window.draw(self.penguin)

        # Handle Pause, Dead, and Game not started states
        if self.substate == Game.DEAD_STATE or self.substate == Game.PAUSE_STATE:
            self.window.screen.blit(self.quit_text_surf, self.quit_text_rect)
            if self.substate == Game.DEAD_STATE:
                self.window.screen.blit(self.restart_text_surf, self.restart_text_rect)
            elif self.substate == Game.PAUSE_STATE:
                self.window.screen.blit(self.unpause_text_surf, self.unpause_text_rect)
                pass
        elif not self.game_started:
            self.window.screen.blit(self.spacebar_text_surf, self.spacebar_text_rect)
            self.window.screen.blit(self.p_to_pause_text_surf, self.p_to_pause_text_rect)

        self.window.screen.blit(self.score_text_surf, self.score_text_rect)

        if self.substate == State.AI_GAME_STATE:
            self.old_state = self.environment_state
            self.environment_state = [self.penguin.y,
                                      self.penguin.velocity,
                                      self.closest_x_distance_to_penguin,
                                      self.closest_gap_range[0],
                                      self.closest_gap_range[1]]
            if self.old_state is None:
                self.old_state = self.environment_state
            if BrainControl.master_brain.get_next_action(self.environment_state):
                self.penguin.flapped()
            BrainControl.master_brain.update(self.old_state, \
                                             self.environment_state, \
                                             0, \
                                             self.reward)

    #
    def keys_pressed_reaction(self):
        if self.substate == State.GAME_STATE:
            if State.is_key_pressed(pygame.K_SPACE):
                if not self.game_started:
                    self.game_started = True
                self.penguin.flapped()
            elif State.is_key_pressed(pygame.K_p) and self.game_started:
                # Pause the game
                self.substate = Game.PAUSE_STATE
        elif self.substate == Game.PAUSE_STATE:
            if State.is_key_pressed(pygame.K_u):
                self.substate = State.GAME_STATE
            elif State.is_key_pressed(pygame.K_q):
                self.state = State.MENU_STATE
        elif self.substate == Game.DEAD_STATE:
            if State.is_key_pressed(pygame.K_p):
                self.state = State.RESTART_STATE
            elif State.is_key_pressed(pygame.K_q):
                self.state = State.MENU_STATE
        elif self.substate == Game.AI_DEAD_STATE:
            self.state = State.AI_RESTART_STATE
