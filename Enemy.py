from DynamicObject import *

class Enemy (DynamicObject):
    def __init__(self, position, sprite, bullet_sprite):
        super().__init__(position, sprite)

        self.bullet_sprite = bullet_sprite
        self.size = pg.Vector2(SHIP_SIZE, SHIP_SIZE)
        self.speed = 200
        self.shooting_timer = 0.5
        self.last_shot = 0
        self.is_explosive = True
        
        # rotate the image
        self.image = pg.transform.scale(self.image, self.size)
        self.image = pg.transform.rotate(self.image, 180)


    def update(self, delta_time):
        super().update(delta_time)


    def render(self, screen):
        super().render(screen)


    def get_dealing_damage(self):
        return self.dealing_damage


    def _ready_to_shoot(self, delta_time):
        self.last_shot += delta_time

        if self.last_shot >= self.shooting_timer:
            self.last_shot = 0
            return True

        return False
    

    def _shoot(self):
        pass