from GameObject import *

class Ship (GameObject):
    def __init__(self, sprite):
        super().__init__(sprite)

        self.size = pg.Vector2(SHIP_SIZE, SHIP_SIZE)
        self.position = pg.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.speed = 500
        self.health = self.max_health = 1000
        self.dealing_damage = 25

        self.initialize()


    def update(self, delta_time):
        super().update(delta_time)

        if self.health <= 0:

            # rotate the image around
            self.image = pg.transform.rotate(self.image, 90)
            self.image = pg.transform.scale(self.image, self.size)

            self.position.y += self.speed * delta_time
            if self.position.y < 0:
                self.alive = False
                print("Game Over")
            
            return

        self.__handle_movement(delta_time)
        


    def render(self, screen):
        super().render(screen)


    def __handle_movement(self, delta_time):
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