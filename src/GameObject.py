from Common import *

class GameObject:
    def __init__(self, sprite=None):
        """
        Initializes the GameObject.
        
        Args:
            sprite (pg.Surface): Sprite of the object.
        """
        self.size = pg.Vector2(0, 0)
        self.position = pg.Vector2(0, 0)
        self.speed = 0
        self.image = sprite if sprite else None
        self.health = self.max_health = 30
        self.max_health = 30
        self.alive = True
        self.rect = None
        self.original_image = self.image.copy()

    def initialize(self):
        """ Further object initialization. """
        self.image = pg.transform.scale(self.image, self.size)
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect() 

    def render(self, screen):
        """
        Renders the object on the screen.

        Args:
            screen (pg.Surface): The screen to render the object on.
        """
        if self.image:
            screen.blit(self.image, self.rect.topleft)

    def update(self, delta_time):
        """
        Updates the object.

        Args:
            delta_time (float): The time passed since the last update.
        """
        self.rect.center = self.position

    def get_rect(self):
        """
        Returns the rect of the object.

        Returns:
            pg.Rect: The rect of the object.
        """
        return self.rect
    
    def update_health(self, damage):
        """
        Updates the health of the object.

        Args:
            damage (int): The amount of damage to apply.
        """
        self.health += damage
        self.health = max(0, min(self.health, self.max_health))

    def clear_health(self):
        """ Clears the health of the object. """
        self.health = 0

    def _handle_event(self, event):
        pass

    def _draw_rect(self, screen):
        pg.draw.rect(screen, COLOR_WHITE, self.rect, 1)

    def _apply_color(self, color):
        """
        Applies a color to the object.

        Args:
            color (tuple): The color to apply.
        """
        colored_image = pg.Surface(self.image.get_size(), flags=pg.SRCALPHA)
        colored_image.fill(color)
        self.image = self.original_image.copy()
        self.image.blit(colored_image, (0, 0), special_flags=pg.BLEND_RGBA_MULT)

    def _reset_color(self):
        """ Resets the color of the object. """
        self.image = self.original_image.copy()