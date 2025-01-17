from Common import *
from Weapon import Weapon

class Ray (Weapon):
    def __init__(self, position, sprite):

        self.sprite_index = 0
        self.sprite_timer = 0
        self.sprite_max_timer = 0.1
        
        self.sprites = []
        self.size = pg.Vector2(18, 32)
        self.sprites_to_render = SCREEN_HEIGHT // self.size.y + 1

        from Engine import Engine
        sprite = Engine._instance.get_sprite(WEAPONS_PATH + "/ray.png")
        
        for i in range(4):
            self.sprites.append(sprite.subsurface(pg.Rect(i * self.size.x, 0, self.size.x, self.size.y)))

        super().__init__(position, self.sprites[0])
        self.size = pg.Vector2(18, 32)

        self.alive_time = 1
        self.dead_by_collision = False

        self.initialize()

    
    def update(self, delta_time):
        super().update(delta_time)

        self.sprite_timer += delta_time
        if self.sprite_timer >= self.sprite_max_timer:
            self.sprite_timer = 0
            self.sprite_index += 1
            if self.sprite_index >= len(self.sprites):
                self.sprite_index = 0


    def render(self, screen):
        self.image = self.sprites[self.sprite_index]
        
        position_y = self.position.y
        screen.blit(self.sprites[self.sprite_index], (self.position.x, position_y))
        
        for i in range(int(self.sprites_to_render)):
            position_y = self.position.y + (i+1) * self.size.y
            screen.blit(self.sprites[self.sprite_index], (self.position.x, position_y))

        self.rect = pg.Rect(self.position.x, self.position.y, self.size.x, self.size.y * self.sprites_to_render)


