import random

from Common import *
from Weapon import Weapon

class Bomb (Weapon):
    def __init__(self, position, sprite, direction):
        """
        Initializes the bomb object.

        Args:
            position (Vector2): The position of the object.
            sprite (pg.Surface): The sprite of the object.
            direction (ObjectDirection): The direction of the object.
        """
        super().__init__(position, sprite)

        self.size = pg.Vector2(BOMB_SIZE, BOMB_SIZE)
        self.position.x = position.x - self.size.x / 2
        self.position.y = position.y - self.size.y / 2
        self.speed = 200
        self.alive_time = 5
        self.dealing_damage = 5
        self.is_explosive = True

        self.velocity = pg.Vector2(25, -100)
        self.gravity = 300

        if direction == ObjectDirection.LEFT:
            self.direction_x = random.randint(2, 5)
        else:
            self.direction_x = random.randint(-5, -2)

        self.initialize()


    def update(self, delta_time):
        super().update(delta_time)

        if self.is_exploding == True:
            return

        # Update velocity in vertical direction (gravity)
        self.velocity.y += self.gravity * delta_time

        # Update velocity in horizontal direction
        direction = pg.Vector2(self.direction_x, 1)
        direction = direction.normalize()
        self.velocity.x = direction.x * self.speed

        # Update position based on velocity
        self.position += self.velocity * delta_time


    def render(self, screen):
        super().render(screen)