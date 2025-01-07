from Weapon import *

class Bullet (Weapon):
    def __init__(self, position, sprite, direction=ObjectDirection.UP):
        super().__init__(position, sprite)

        self.direction = direction
        self.size = pg.Vector2(BULLET_SIZE, BULLET_SIZE)
        self.position.x = position.x - self.size.x / 2
        self.position.y = position.y - self.size.y / 2
        self.speed = 400


        if self.direction == ObjectDirection.DOWN:
            # rotate the image
            self.image = pg.transform.scale(self.image, self.size)
            self.image = pg.transform.rotate(self.image, 180)

        self.initialize()


    def update(self, delta_time):
        super().update(delta_time)

        direction = pg.Vector2(1, -1)

        if self.direction == ObjectDirection.DOWN:
            direction = pg.Vector2(1, 1)

        self.position.y += direction.y * self.speed * delta_time


    def render(self, screen):
        super().render(screen)