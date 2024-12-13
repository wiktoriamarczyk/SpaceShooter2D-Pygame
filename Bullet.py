from GameObject import *

class Bullet (GameObject):
    def __init__(self, position_x, position_y):
        super().__init__()
        image_path = DATA_PATH + 'sprites/bullet.png'
        self.image = pg.image.load(image_path) if image_path else None
        self.size = pg.Vector2(10, 10)
        self.position.x = position_x - self.size.x / 2
        self.position.y = position_y - self.size.y / 2
        self.speed = 400

        self.initialize()


    def update(self, delta_time):
        super().update(delta_time)

        direction = pg.Vector2(1, -1)
        self.position.y += direction.y * self.speed * delta_time

        if (self.position.y > SCREEN_HEIGHT or self.position.y < 0 
            or self.position.x < 0 or self.position.x > SCREEN_WIDTH):
            self.alive = False


    def render(self, screen):
        super().render(screen)