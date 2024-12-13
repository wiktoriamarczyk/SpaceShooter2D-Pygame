from DynamicObject import *

class BasicEnemy (DynamicObject):
    def __init__(self, position, sprite_path):
        super().__init__(position, sprite_path)

        self.size = pg.Vector2(SHIP_SIZE, SHIP_SIZE)
        self.speed = 200
        
        # rotate the image
        self.image = pg.transform.scale(self.image, self.size)
        self.image = pg.transform.rotate(self.image, 180)

        self.initialize()


    def update(self, delta_time):
        super().update(delta_time)

        # move down
        self.position.y += self.speed * delta_time


    def render(self, screen):
        super().render(screen)