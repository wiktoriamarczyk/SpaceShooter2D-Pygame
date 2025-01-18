from Common import *
from Enemy import Enemy

class TargetingEnemy (Enemy):
    def __init__(self, position, sprite):
        
        from Engine import Engine
        path = os.path.join(WEAPONS_PATH, 'torpedo0.png')
        bullet_sprite = Engine._instance.get_sprite(path)
        
        super().__init__(position, sprite, bullet_sprite)

        self.speed = 250
        self.shooting_timer = 2
        self.health = self.max_health = 50

        self.init_health_bar()
        
        self.initialize()


    def update(self, delta_time):
        super().update(delta_time)

        if self.is_exploding == True:
            return

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