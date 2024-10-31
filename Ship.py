from GameObject import *

class Ship (GameObject):
    def __init__(self):
        super().__init__()
        image_path = DATA_PATH + 'sprites/ship-base.png'
        self.image = pg.image.load(image_path) if image_path else None
        self.size = pg.Vector2(100, 100)
        # set position to the center of the screen with pivot in the center
        self.position = pg.Vector2(SCREEN_WIDTH / 2 - self.size.x / 2, SCREEN_HEIGHT / 2 - self.size.y / 2)
        self.image = pg.transform.scale(self.image, self.size)
        self.speed = 200


    def update(self, delta_time):
        self.handle_movement(delta_time)


    def handle_movement(self, delta_time):
        keys = pg.key.get_pressed()  
        direction = pg.Vector2(1, -1)
        
        if keys[pg.K_UP]:
            self.position.y += direction.y * self.speed * delta_time
        if keys[pg.K_DOWN]:
            self.position.y -= direction.y * self.speed * delta_time
        if keys[pg.K_LEFT]:
            self.position.x -= direction.x * self.speed * delta_time
        if keys[pg.K_RIGHT]:
            self.position.x += direction.x * self.speed * delta_time


    def render(self, screen):
        super().render(screen)