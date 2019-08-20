import pygame, sys
from src.Entity import ImageEntity


class Penguin(ImageEntity):
    image_alive = "Penguino_ALIVE.png"
    gravity = 0.3
    flap_velocity = 9

    def __init__(self, x, y, name="Penguin"):
        self.name = name
        self.alive = True
        self.velocity = 0.0
        ImageEntity.__init__(self, Penguin.image_alive, x, y, name)
        self.image_width = self.image.get_width()
        self.image_height = self.image.get_height()

    def move(self):
        if self.velocity < 10:
            self.velocity += Penguin.gravity
        self.y += self.velocity

    def flapped(self):
        self.velocity /= 1.5
        self.velocity -= Penguin.flap_velocity

    def is_collided_with(self, entity):
        entity_x = entity.x;
        entity_y = entity.y;
        entity_width = entity.get_width()
        entity_height = entity.get_width()

        entity_collision_range_x = (entity_x - entity_width, entity_x + (entity_width))
        x_collision = (entity_collision_range_x[0] < self.x < entity_collision_range_x[1])

        entity_collision_range_y = (entity_y - entity_height, entity_y + (entity_height / 2))
        y_collision = (entity_collision_range_y[0] < self.y < entity_collision_range_y[1])

        return x_collision and y_collision