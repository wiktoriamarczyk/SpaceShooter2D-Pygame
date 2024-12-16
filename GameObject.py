from Common import *

class GameObject:
    def __init__(self, sprite=None):
        self.size = pg.Vector2(0, 0)
        self.position = pg.Vector2(0, 0)
        self.speed = 0
        self.image = sprite if sprite else None
        self.alive = True
        self.rect = None

    def __del__(self):
        pass

    def initialize(self):
        self.image = pg.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect() 

    def render(self, screen):
        if self.image:
            screen.blit(self.image, self.rect.topleft)

    def update(self, delta_time):
        self.rect.center = self.position

    def _handle_event(self, event):
        pass

    def _draw_rect(self, screen):
        pg.draw.rect(screen, (255, 255, 255), self.rect, 1)

    def _apply_color(self):
        """
        Applies the specified color to the image using a blend mode.
        """
        colored_image = pg.Surface(self.image.get_size(), flags=pg.SRCALPHA)
        colored_image.fill(self.color)  # Wypełnienie kolorem

        self.image.blit(colored_image, (0, 0), special_flags=pg.BLEND_RGBA_MULT)