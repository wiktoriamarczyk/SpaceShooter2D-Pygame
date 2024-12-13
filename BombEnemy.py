import math
from Enemy import *

class BombEnemy (Enemy):
    def __init__(self, position):
        super().__init__(position)

        image_path = DATA_PATH + 'sprites/bomb-ship.png'
        self.image = pg.image.load(image_path) if image_path else None
        self.size = pg.Vector2(SHIP_SIZE, SHIP_SIZE)
        self.position = position
        self.speed = 200
        self.timer = 0

        # rotate the image
        self.image = pg.transform.scale(self.image, self.size)
        self.image = pg.transform.rotate(self.image, 180)

        self.initialize()


    def update(self, delta_time):
        super().update(delta_time)
        self.timer += delta_time

        # move sin wave
        self.position.y += self.speed * delta_time
        self.position.x += math.sin(self.timer * 5) * 200 * delta_time


    def render(self, screen):
        super().render(screen)