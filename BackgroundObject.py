from DynamicObject import *

class BackgroundObject (DynamicObject):
    def __init__(self, position, sprite_path):
        super().__init__(position, sprite_path)

        self.size = pg.Vector2(SHIP_SIZE, SHIP_SIZE)


    def update(self, delta_time):
        super().update(delta_time)

        # check if the object is out of bounds
        if (self.position.y > SCREEN_HEIGHT or self.position.x < 0 or self.position.x > SCREEN_WIDTH):
            self.alive = False


    def render(self, screen):
        super().render(screen)