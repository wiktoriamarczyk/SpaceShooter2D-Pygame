from Common import *
from DynamicObject import DynamicObject
from HealthBar import HealthBar

class Enemy (DynamicObject):
    def __init__(self, position, sprite, bullet_sprite, rotate = 180):
        """
        Initializes the enemy object.

        Args:
            position (Vector2): The position of the enemy.
            sprite (pg.Surface): The sprite of the enemy.
            bullet_sprite (pg.Surface): The sprite of the bullet.
            rotate (int): The rotation angle of the enemy.
        """
        super().__init__(position, sprite)

        self.bullet_sprite = bullet_sprite
        self.size = pg.Vector2(SHIP_SIZE, SHIP_SIZE)
        self.speed = 200
        self.shooting_timer = 0.5
        self.last_shot = 0
        self.is_explosive = True

        # rotate the image
        self.image = pg.transform.scale(self.image, self.size)
        self.image = pg.transform.rotate(self.image, rotate)


    def init_health_bar(self, width = 50, height = 10):
        """
        Initialize the health bar for the enemy.

        Args:
            width (int): The width of the health bar.
            height (int): The height of the health bar.
        """
        self.health_bar = HealthBar(width, height, self.max_health)


    def update(self, delta_time):
        super().update(delta_time)


    def render(self, screen):
        super().render(screen)
        
        enemy_bar_x = int(self.position.x - self.health_bar.width / 2)
        offset_y = 10
        enemy_bar_y = int(self.position.y - self.size.y / 2 - offset_y)
        self.health_bar.draw(screen, pg.Vector2(enemy_bar_x, enemy_bar_y), self.health)


    def get_dealing_damage(self):
        """
        Get the damage that the enemy deals.

        Returns:
            int: The damage that the enemy deals.
        """
        return self.dealing_damage


    def _ready_to_shoot(self, delta_time):
        """
        Check if the enemy is ready to shoot.

        Args:
            delta_time (float): The time passed since the last frame.

        Returns:
            bool: True if the enemy is ready to shoot, False otherwise.
        """
        self.last_shot += delta_time

        if self.last_shot >= self.shooting_timer:
            self.last_shot = 0
            return True

        return False
    

    def _shoot(self):
        """
        Shoot a bullet.
        """
        pass