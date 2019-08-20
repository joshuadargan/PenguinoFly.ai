import pygame


# Base class for all entities. (i.e. Everything that moves and has an image)
class Entity:
    assets_folder = "Assets/"

    def __init__(self, x, y, name):
        self.name = name
        self.x = x
        self.y = y

    # Moves x and y location by velocity
    def move(self, x_vel, y_vel):
        self.x += x_vel
        self.y += y_vel

    # Each class that inherits Entity needs to override this method if they want to use it
    def move(self):
        pass

    def set_x(self, x_location):
        self.x = x_location

    def set_y(self, y_location):
        self.y = y_location

    # Returns x and y location in form of a tuple
    def get_location(self):
        return (self.x,self.y)

    def get_entity(self):
        return self

    def get_width(self):
        return 0

    def get_height(self):
        return 0

class ImageEntity(Entity):
    assets_folder = "Assets/"

    def __init__(self, image_name, x, y, name):
        self.image = pygame.image.load(Entity.assets_folder + image_name)
        self.name = name
        self.x = x
        self.y = y

    def get_width(self):
        return self.image.get_width()

    def get_height(self):
        return self.image.get_height()