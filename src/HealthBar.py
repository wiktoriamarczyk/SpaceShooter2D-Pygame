from Common import *

class HealthBar:
    def __init__(self, width, height, max_health):
        """
        Initializes the health bar object.

        Args:
            width (int): The width of the health bar.
            height (int): The height of the health bar.
            max_health (int): The maximum health of the entity.
        """
        self.width = width
        self.height = height
        self.max_health = max_health

        self.foreground_color = (0, 255, 0)
        self.background_color = (100, 100, 100)
        self.border_color = (255, 255, 255)


    def draw(self, screen, position, current_health):
        """
        Draws the health bar on the screen.

        Args:
            screen (pygame.Surface): The surface to draw the health bar on.
            position (Vector2): The position to draw the health bar at.
            current_health (int): The current health of the entity.
        """
        health_percentage = max(0, current_health / self.max_health)
        current_bar_width = int(self.width * health_percentage)

        pg.draw.rect(screen, (100, 100, 100), (position.x, position.y, self.width, self.height))  # Background
        pg.draw.rect(screen, (0, 255, 0), (position.x, position.y, current_bar_width, self.height))  # Foreground
        pg.draw.rect(screen, (255, 255, 255), (position.x, position.y, self.width, self.height), 2) # Border
        