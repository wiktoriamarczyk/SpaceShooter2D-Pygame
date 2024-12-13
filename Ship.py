from GameObject import *

class Ship (GameObject):
    def __init__(self):
        super().__init__()
        image_path = DATA_PATH + 'sprites/ship.png'
        self.image = pg.image.load(image_path) if image_path else None
        self.size = pg.Vector2(SHIP_SIZE, SHIP_SIZE)
        self.position = pg.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.speed = 300

        self.initialize()


    def update(self, delta_time):
        super().update(delta_time)
        self.handle_movement(delta_time)


    def handle_movement(self, delta_time):
        keys = pg.key.get_pressed()  
        direction = pg.Vector2(1, -1)

        if keys[pg.K_UP] and self.position.y > 0 + SHIP_SIZE / 2:
            self.position.y += direction.y * self.speed * delta_time
        if keys[pg.K_DOWN] and self.position.y < SCREEN_HEIGHT - SHIP_SIZE / 2:
            self.position.y -= direction.y * self.speed * delta_time
        if keys[pg.K_LEFT] and self.position.x > 0 + SHIP_SIZE / 2:
            self.position.x -= direction.x * self.speed * delta_time
        if keys[pg.K_RIGHT] and self.position.x < SCREEN_WIDTH - SHIP_SIZE / 2:
            self.position.x += direction.x * self.speed * delta_time


    def render(self, screen):
        super().render(screen)