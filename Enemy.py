from GameObject import *
from Common import *

class Enemy (GameObject):
    def __init__(self, position):
        super().__init__()


    def update(self, delta_time):
        super().update(delta_time)

        # check if the enemy is out of bounds
        if (self.position.y > SCREEN_HEIGHT or self.position.x < 0 or self.position.x > SCREEN_WIDTH):
            self.alive = False


    def render(self, screen):
        super().render(screen)