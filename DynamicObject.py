from Common import *
from GameObject import GameObject

class DynamicObject (GameObject):
    def __init__(self, position, sprite):
        super().__init__(sprite)

        self.position = position
        self.speed = 100
        self.timer = 0
        self.alive_time = None
        self.death_by_time = False

        # Explosion animation parameters
        from Engine import Engine
        self.explosion_frames = [
            Engine._instance.get_sprite(WEAPONS_PATH + "/explosion1.png"),
            Engine._instance.get_sprite(WEAPONS_PATH + "/explosion2.png"),
            Engine._instance.get_sprite(WEAPONS_PATH + "/explosion3.png"),
            Engine._instance.get_sprite(WEAPONS_PATH + "/explosion4.png"),
            Engine._instance.get_sprite(WEAPONS_PATH + "/explosion5.png"),
        ]
        self.is_explosive = False
        self.is_exploding = False
        self.explosion_frame_index = 0
        self.explosion_frame_time = 0.1  # Time per frame in seconds
        self.explosion_timer = 0
    

    def update_explosion_logic(self, delta_time):
        if self.is_exploding == True:
            self.image = self.explosion_frames[self.explosion_frame_index]
            self.image = pg.transform.scale(self.image, self.size)
            self.image.blit(self.image, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
            self.explosion_timer += delta_time
            if self.explosion_timer >= self.explosion_frame_time:
                self.explosion_timer = 0
                # Change to the next explosion frame
                self.explosion_frame_index += 1
                # After the last frame, the bomb is dead
                if self.explosion_frame_index >= len(self.explosion_frames):
                    self.alive = False
                    return True
                # Change the image to the next frame
                if self.explosion_frame_index < len(self.explosion_frames):
                    self.image = self.explosion_frames[self.explosion_frame_index]
                    self.image = pg.transform.scale(self.image, self.size)
                    self.image.blit(self.image, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
            return True
        

    def update(self, delta_time):
        super().update(delta_time)

        # check if the object is out of bounds
        if (self.position.y > SCREEN_HEIGHT + self.size.y or self.position.x < 0 - self.size.x or self.position.x > SCREEN_WIDTH + self.size.x):
            self.alive = False

        # if the object has an alive time, decrease it and check if its lifetime has ended
        if self.alive_time is not None:
            self.alive_time -= delta_time

        # if lifetime has ended or health is 0, the object is dead or ready to explode
        if (((self.alive_time is not None and self.alive_time <= 0) or self.health <= 0) and self.is_explosive == False):
            self.alive = False
            self.death_by_time = True

        elif (((self.alive_time is not None and self.alive_time <= 0) or self.health <= 0) and self.is_explosive == True):
            self.is_exploding = True
            self.update_explosion_logic(delta_time)
            self.death_by_time = True


    def render(self, screen):
        super().render(screen)