import random

from Common import *
from Enemy import Enemy

class Boss (Enemy):
    def __init__(self, position, sprite):
        
        super().__init__(position, sprite, None)
        
        self.health = self.max_health = 500
        self.speed = 50
        self.shooting_timer = 3
        self.size = pg.Vector2(BOSS_SIZE, BOSS_SIZE)

        self.init_health_bar(150, 10)
        self.initialize()


    def update(self, delta_time):
        super().update(delta_time)

        if self.is_exploding == True:
            from Engine import Engine
            Engine._instance.set_game_over(False)

        if self.position.y < self.size.y:
            self.position.y += self.speed * delta_time

        if super()._ready_to_shoot(delta_time):
                self._shoot()
                self.shooting_timer = random.randint(2, 3)


    def _shoot(self):
        super()._shoot()

        from Engine import Engine
        from Ray import Ray

        offset = pg.Vector2(10, 20)
        ray = Ray(pg.Vector2(self.position.x - offset.x, self.position.y + self.size.y / 2 - offset.y), None)
        Engine._instance.add_object(ray)


    def render(self, screen):
        super().render(screen)