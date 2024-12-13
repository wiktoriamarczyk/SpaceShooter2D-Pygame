from GameObject import *

class Bullet (GameObject):
    def __init__(self, input_position, sprite_path):
        super().__init__(sprite_path)

        self.size = pg.Vector2(10, 10)
        self.position.x = input_position.x - self.size.x / 2
        self.position.y = input_position.y - self.size.y / 2
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