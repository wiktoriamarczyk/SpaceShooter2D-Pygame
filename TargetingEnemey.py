import math
from Enemy import *


class TargetingEnemy (Enemy):
    def __init__(self, position, sprite):
        
        from Engine import Engine
        bullet_sprite = Engine._instance.get_bullet_texture("torpedo0.png")
        
        super().__init__(position, sprite, bullet_sprite)
        self.speed = 300

        self.initialize()


    def update(self, delta_time):
        super().update(delta_time)
        self.timer += delta_time

        # move down
        self.position.y += self.speed * delta_time

        if super()._ready_to_shoot(delta_time):
            self._shoot()


    def _shoot(self):
        super()._shoot()
        
        from Engine import Engine
        from HomingMissile import HomingMissile
        
        target = Engine._instance.get_ship_position()
        missile = HomingMissile(pg.Vector2(self.position.x, self.position.y), self.bullet_sprite, target)
        Engine._instance.add_object(missile)
        

    def render(self, screen):
        super().render(screen)