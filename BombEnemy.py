import math
from Enemy import *


class BombEnemy (Enemy):
    def __init__(self, position, sprite):
        
        from Engine import Engine
        bullet_sprite = Engine._instance.get_bullet_texture("bomb-ship-weapon.png")
        
        super().__init__(position, sprite, bullet_sprite)

        self.initialize()


    def update(self, delta_time):
        super().update(delta_time)
        self.timer += delta_time

        # move sin wave
        self.position.y += self.speed * delta_time
        self.position.x += math.sin(self.timer * 5) * 200 * delta_time


    def render(self, screen):
        super().render(screen)