from GameObject import *
from Common import *

class DynamicObject (GameObject):
    def __init__(self, position, sprite_path):
        super().__init__(sprite_path)

        self.position = position
        self.speed = 100
        self.timer = 0


    def update(self, delta_time):
        super().update(delta_time)

        # check if the object is out of bounds
        if (self.position.y > SCREEN_HEIGHT or self.position.x < 0 or self.position.x > SCREEN_WIDTH):
            self.alive = False


    def render(self, screen):
        super().render(screen)