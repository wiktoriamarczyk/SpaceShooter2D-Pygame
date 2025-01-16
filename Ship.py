from GameObject import *
from HealthBar import *

class Ship (GameObject):
    def __init__(self, sprite):
        super().__init__(sprite)

        self.size = pg.Vector2(SHIP_SIZE, SHIP_SIZE)
        self.position = pg.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.speed = 500
        self.health = self.max_health = 1000
        self.dealing_damage = 25
        self.health_bar = HealthBar(200, 20, self.max_health)
        self.shield_timer = 0
        self.shield_color = (65, 105, 225)

        self.initialize()


    def update(self, delta_time):
        super().update(delta_time)
        print(self.position)

        if self.shield_timer > 0:
            self._apply_color(self.shield_color)
            self.shield_timer -= delta_time
        else:
            self._reset_color()

        if self.health <= 0:
            # rotate the image around
            self.image = pg.transform.rotate(self.image, 90)
            self.image = pg.transform.scale(self.image, self.size)

            self.position.y += self.speed * delta_time
            if self.position.y < 0:
                self.alive = False
                
                from Engine import Engine
                Engine._instance.set_game_over(False)

            return

        self.__handle_movement(delta_time)


    def update_health(self, damage):
        if self.shield_timer > 0:
            return
        return super().update_health(damage)
        

    def render(self, screen):
        super().render(screen)
        # Render health bar on top of the screen
        health_bar_pos = pg.Vector2(10, 10)
        self.health_bar.draw(screen, health_bar_pos, self.health)

    
    def activate_shield_defense(self, time):
        if self.health <= 0:
            return
        self.shield_timer = time


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