import math
from Weapon import *

class HomingMissile (Weapon):
    def __init__(self, position, sprite, target):
        super().__init__(position, sprite)

        self.target = target
        self.size = pg.Vector2(BOMB_SIZE, BOMB_SIZE)
        self.position.x = position.x - self.size.x / 2
        self.position.y = position.y - self.size.y / 2
        self.speed = 300
        self.alive_time = 3
        self.dealing_damage = 15
        self.is_explosive = True

        # Precompute rotations
        self.original_image = self.image
        self.rotated_images = [pg.transform.rotate(self.original_image, angle) for angle in range(0, 360, 5)]

        # Parameters for arc movement
        self.oscillation_frequency = 2
        self.amplitude = 50
        self.time = 0

        self.initialize()


    def get_rotated_image(self, angle):
        index = int(angle / 5) % len(self.rotated_images)
        return self.rotated_images[index]


    def update(self, delta_time):
        super().update(delta_time)

        if self.is_exploding == True:
            return

        direction = (self.target - self.position).normalize()

        # Rotate the image
        angle = math.degrees(math.atan2(direction.y, direction.x))
        self.image = self.get_rotated_image(-angle)

        # Move towards the target
        self.position += direction * self.speed * delta_time

        # Add oscillation in perpendicular motion
        self.time += delta_time
        perp_direction = pg.Vector2(-direction.y, direction.x)  # Perpendicular vector
        self.position += perp_direction * math.sin(self.time * self.oscillation_frequency) * self.amplitude * delta_time

        # Check if the bomb has reached the target
        if self.position.distance_to(self.target) < self.size.x:
            self.alive = False


    def render(self, screen):
        super().render(screen)