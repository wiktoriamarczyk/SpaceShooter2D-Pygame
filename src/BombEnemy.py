import math

from Common import *
from Enemy import Enemy

class BombEnemy (Enemy):
    def __init__(self, position, sprite):
        
        from Engine import Engine
        path = os.path.join(WEAPONS_PATH, 'bomb-ship-weapon.png')
        bullet_sprite = Engine._instance.get_sprite(path)
        
        super().__init__(position, sprite, bullet_sprite)

        self.start_position = position
        self.direction = ObjectDirection.LEFT
        self.shooting_timer = 0.75
        self.health = self.max_health = 40

        self.init_health_bar()

        self.initialize()


    def update(self, delta_time):
        super().update(delta_time)

        if self.is_exploding == True:
            return
        
        self.timer += delta_time

        # move sin wave
        self.position.y += self.speed * delta_time
        horizontal_displacement = math.sin(self.timer * 5) * 200 * delta_time
        self.position.x += horizontal_displacement

        if horizontal_displacement > 0:
            self.direction = ObjectDirection.RIGHT
        elif horizontal_displacement < 0:
            self.direction = ObjectDirection.LEFT

        if super()._ready_to_shoot(delta_time):
            self._shoot()


    def _shoot(self):
        super()._shoot()
        
        from Engine import Engine
        from Bomb import Bomb
        
        bomb = Bomb(pg.Vector2(self.position.x, self.position.y), self.bullet_sprite, self.direction)
        Engine._instance.add_object(bomb)
        

    def render(self, screen):
        super().render(screen)