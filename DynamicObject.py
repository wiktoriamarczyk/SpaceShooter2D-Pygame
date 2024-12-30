from GameObject import *
from Common import *

class DynamicObject (GameObject):
    def __init__(self, position, sprite):
        super().__init__(sprite)

        self.position = position
        self.speed = 100
        self.timer = 0
        self.alive_time = None


    def update(self, delta_time):
        super().update(delta_time)

        # check if the object is out of bounds
        if (self.position.y > SCREEN_HEIGHT + self.size.y or self.position.x < 0 - self.size.x or self.position.x > SCREEN_WIDTH + self.size.x):
            self.alive = False

        # if the object has an alive time, decrease it and check if its lifetime has ended
        if self.alive_time is not None:
            self.alive_time -= delta_time

            if self.alive_time <= 0:
                self.alive = False


    def render(self, screen):
        super().render(screen)