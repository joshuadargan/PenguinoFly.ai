import pygame, sys
from src.Entity import Entity
from src.Entity import ImageEntity
import random


class Ice(ImageEntity):
    image_base = "Icicle.png"
    image_top = "Icicle_TOP.png"
    image_bottom = "Icicle_BOTTOM.png"
    icicle_type = "icicle"
    ceiling_type = "ceiling"
    floor_type = "floor"
    x_vel = 4
    image_height = 50
    image_width = 100

    @staticmethod
    def base():
        x = 0

    def __init__(self, image_name, x, y, name=icicle_type):
        ImageEntity.__init__(self, image_name, x, y, name)

    def move(self):
        self.x -= Ice.x_vel


class IceBoundary:

    def __init__(self, screen_width, screen_height):
        self.floor_height = screen_height - Ice.image_height
        self.ceiling_height = 0

        self.floor = []
        self.ceiling = []
        x_location = Icicle.neg_gap_size # Makes it start off screen
        while x_location < screen_width:
            self.floor.append(Ice(Ice.image_top, x_location, self.floor_height, Ice.floor_type))
            self.ceiling.append(Ice(Ice.image_bottom, x_location, self.ceiling_height, Ice.ceiling_type))
            x_location += Ice.image_width


class Icicle(Entity):
    gap_size = 250
    neg_gap_size = -750
    name = "Icicle"

    def __init__(self, screen_width, screen_height):
        Entity.__init__(self, screen_width, 0, Icicle.name)
        # Take off 7 for a buffer on the bottom

        self.counted = False

        self.ice_blocks = []
        # at what point in num_blocks we add the gap
        num_possible_gaps = int(screen_height / Ice.image_height) - 6
        gap = random.randint(1, num_possible_gaps)
        num_blocks = 0
        height = 0

        while height < screen_height:
            # Add the middle pieces if we reach the gap point
            if num_blocks == gap:
                self.ice_blocks.append(Ice(Ice.image_bottom, screen_width, height, Ice.icicle_type))

                top = height
                height += Icicle.gap_size
                bottom = height
                self.gap_range = (top, bottom)

                self.ice_blocks.append(Ice(Ice.image_top, screen_width, height, Ice.icicle_type))
            else:
                self.ice_blocks.append(Ice(Ice.image_base, screen_width, height, Ice.icicle_type))

            num_blocks += 1
            height += Ice.image_height

    def move(self):
        for iceBlock in self.ice_blocks:
            iceBlock.move()
        self.x -=  Ice.x_vel

    def get_entity(self):
        return self.ice_blocks

    def is_counted(self):
        return self.counted

    def scored(self):
        self.counted = True