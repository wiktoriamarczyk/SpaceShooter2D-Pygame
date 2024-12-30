from DynamicObject import *

class TemporaryDynamicObject (DynamicObject):
    def __init__(self, position, sprite):
        super().__init__(position, sprite)

        self.alive_time = 5


    def update(self, delta_time):
        super().update(delta_time)

        self.timer -= delta_time

        if self.timer <= 0:
            self.alive = False
        

    def render(self, screen):
        super().render(screen)