from Common import *

class GameObject:
    def __init__(self):
        self.position = pg.Vector2(0, 0)
        self.size = pg.Vector2(0, 0)
        self.image = None
        self.speed = 0
        self.alive = True

    def render(self, screen):
        if self.image:
            screen.blit(self.image, self.position)

    def update(self, delta_time):
        pass

    def handle_event(self, event):
        pass

    def __del__(self):
        print("deleting..." + __name__)