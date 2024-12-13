from Common import *

class GameObject:
    def __init__(self, sprite_path=None):
        self.size = pg.Vector2(0, 0)
        self.position = pg.Vector2(0, 0)
        self.speed = 0
        self.image = sprite_path if sprite_path else None
        self.alive = True
        self.rect = None

    def initialize(self):
        self.image = pg.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect() 

    def render(self, screen):
        if self.image:
            screen.blit(self.image, self.rect.topleft)

    def update(self, delta_time):
        self.rect.center = self.position

    def handle_event(self, event):
        pass

    def __del__(self):
        pass

    def draw_rect(self, screen):
        pg.draw.rect(screen, (255, 255, 255), self.rect, 1)