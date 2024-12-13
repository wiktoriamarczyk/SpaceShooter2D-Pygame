from Enemy import *

class BasicEnemy (Enemy):
    def __init__(self, position):
        super().__init__(position)
        image_path = DATA_PATH + 'sprites/bullet-ship.png'
        self.image = pg.image.load(image_path) if image_path else None
        self.size = pg.Vector2(SHIP_SIZE, SHIP_SIZE)
        self.position = position
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