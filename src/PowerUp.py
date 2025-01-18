from Common import *
from DynamicObject import DynamicObject

class PowerUp (DynamicObject):
    def __init__(self, position, sprite, direction, type):
        """
        Initializes the power up object.

        Args:
            position (Vector2): The position of the object.
            sprite (pg.Surface): The sprite of the object.
            direction (ObjectDirection): The direction of the object.
            type (PowerUpType): The type of the power up.
        """
        super().__init__(position, sprite)

        self.direction = direction
        self.size = pg.Vector2(POWER_UP_SIZE, POWER_UP_SIZE)
        self.type = type
        self.velocity = pg.Vector2(25, -100)
        self.gravity = 300

        if direction == ObjectDirection.LEFT:
            self.direction_x = -20
        else:
            self.direction_x = 20

        self.initialize()


    def update(self, delta_time):
        super().update(delta_time)

        # Update velocity in vertical direction (gravity)
        self.velocity.y += self.gravity * delta_time

        # Update velocity in horizontal direction
        direction = pg.Vector2(self.direction_x, 1)
        direction = direction.normalize()
        self.velocity.x = direction.x * self.speed

        # Update position based on velocity
        self.position += self.velocity * delta_time


    def draw(self):
        super().draw()