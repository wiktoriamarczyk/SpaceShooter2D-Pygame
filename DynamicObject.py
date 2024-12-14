from GameObject import *
from Common import *

class DynamicObject (GameObject):
    def __init__(self, position, sprite):
        super().__init__(sprite)

        self.position = position
        self.speed = 100
        self.timer = 0


    def update(self, delta_time):
        super().update(delta_time)

        # check if the object is out of bounds
        if (self.position.y > SCREEN_HEIGHT + self.size.y or self.position.x < 0 - self.size.x or self.position.x > SCREEN_WIDTH + self.size.x):
            self.alive = False


    def render(self, screen):
        super().render(screen)