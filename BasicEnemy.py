from Enemy import *

class BasicEnemy (Enemy):
    def __init__(self, position, sprite):

        from Engine import Engine
        bullet_sprite = Engine._instance.get_bullet_texture("bullet-ship-weapon.png")

        super().__init__(position, sprite, bullet_sprite)

        self.initialize()


    def update(self, delta_time):
        super().update(delta_time)

        # move down
        self.position.y += self.speed * delta_time

        if super()._ready_to_shoot(delta_time):
            self._shoot()


    def _shoot(self):
        from Engine import Engine
        from Bullet import Bullet

        bullet_offset = 10
        bullet1 = Bullet(pg.Vector2(self.position.x - bullet_offset, self.position.y + bullet_offset), self.bullet_sprite, ObjectDirection.DOWN)
        bullet2 = Bullet(pg.Vector2(self.position.x + 3 * bullet_offset, self.position.y + bullet_offset), self.bullet_sprite, ObjectDirection.DOWN)

        Engine._instance.add_object(bullet1)
        Engine._instance.add_object(bullet2)


    def render(self, screen):
        super().render(screen)