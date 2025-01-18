from DynamicObject import DynamicObject

class BackgroundObject (DynamicObject):
    def __init__(self, position, sprite, size, depth, color=None):
        """
        Initializes the background object.

        Args:
            position (Vector2): The position of the object.
            sprite (pg.Surface): The sprite of the object.
            size (int): The size of the object.
            depth (int): The depth of the object.
            color (tuple): The color of the object.
        """
        super().__init__(position, sprite)

        self.size = size * 0.5 * depth
        self.speed = self.speed / depth
        self.color = color

        # color the image
        if self.color is not None:
            self._apply_color(self.color)

        self.initialize()


    def update(self, delta_time):
        super().update(delta_time)

        # move down
        self.position.y += self.speed * delta_time


    def render(self, screen):
        super().render(screen)