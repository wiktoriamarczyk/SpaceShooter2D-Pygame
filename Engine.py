import os
import random
import time
from Common import *
from Ship import *
from Bullet import *
from BasicEnemy import *
from BombEnemy import *
from BackgroundObject import *

class Engine:
    def __init__(self):
        # main variables
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pg.time.Clock()
        self.frame_per_sec = 60.0
        
        # units
        self.game_objects = []
        self.ship = None
        self.enemy_type = BasicEnemy

        # time variables
        self.init_time_variables()

        # resources
        self.units_sprites = []
        self.weapon_sprites = []
        self.asteroids_sprites = []
        self.stars_sprites = []
        self.load_all_images()

        self.spawn_init_stars()
        self.init_game_objects()


    def run(self):
        while True:
            self.handle_events()
            self.screen.fill(BACKGROUND_COLOR)
            self.clock.tick(self.frame_per_sec)
            delta_time = 1.0 / self.frame_per_sec
            self.update(delta_time)
            self.render()
            # update the display
            pg.display.flip()


    def handle_events(self):
        for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYUP:
                     if event.key == pg.K_SPACE:
                        self.fire_bullet()


    def render(self):
        for game_object in self.game_objects:
            game_object.render(self.screen)
        self.ship.render(self.screen)


    def update(self, delta_time):
        current_time = time.time()

        # remove dead game objects
        for go in self.game_objects:
            if go.alive == False:
                self.game_objects.remove(go)
                go.__del__()

        self.spawn_time_objects(current_time)

        for game_object in self.game_objects:
            game_object.update(delta_time)
        self.ship.update(delta_time)


    def fire_bullet(self):
        bullet_pos = self.ship.position
        bullet = Bullet(pg.Vector2(bullet_pos.x + 5, bullet_pos.y - 10), self.weapon_sprites['bullet.png'])
        self.game_objects.append(bullet)


    def spawn_enemy(self):
        x_position = random.randint(2*SHIP_SIZE, SCREEN_WIDTH - 2*SHIP_SIZE)
        
        sprite_path = "bullet-ship.png"
        if self.enemy_type == BombEnemy:
            sprite_path = "bomb-ship.png"

        enemy = self.enemy_type(pg.Vector2(x_position, -SHIP_SIZE), self.units_sprites[sprite_path])
        self.game_objects.append(enemy)

    # ----------------- Background objects -----------------

    def spawn_background_object(self, sprite_list, position, size_range, depth_range, color=None):
        """
        Spawns a generic background object.

        Args:
            sprite_list (dict): Dictionary of sprites to choose from.
            position (pg.Vector2): Initial position of the object.
            size_range (tuple): Minimum and maximum size of the object (min_size, max_size).
            depth_range (tuple): Minimum and maximum depth of the object (min_depth, max_depth).
            color (pg.Color): Color of the object.
        """
        depth = random.randint(*depth_range)
        size = random.randint(*size_range)
        sprite_image = random.choice(list(sprite_list.values()))
        background_object = BackgroundObject(position, sprite_image, pg.Vector2(size, size), depth, color)
        self.game_objects.append(background_object)


    def spawn_asteroids(self):
        """Spawns an asteroid."""
        size_range = (ASTEROID_SIZE // 2, ASTEROID_SIZE)
        depth_range = (1, 2)
        x_position = random.randint(2 * ASTEROID_SIZE, SCREEN_WIDTH - 2 * ASTEROID_SIZE)
        position = pg.Vector2(x_position, -ASTEROID_SIZE)
        self.spawn_background_object(self.asteroids_sprites, position, size_range, depth_range)


    def spawn_star(self, position):
        """Spawns a single star at the specified position."""
        color=None
        if random.randint(1, 5) == 4:
            color = random.choice(STAR_COLORS)
        size_range = (STAR_SIZE // 2, STAR_SIZE)
        depth_range = (1, 2)
        self.spawn_background_object(self.stars_sprites, position, size_range, depth_range, color)


    def spawn_init_stars(self):
        """Spawns initial stars randomly across the screen."""
        for _ in range(25):
            x_position = random.randint(STAR_SIZE, SCREEN_WIDTH - STAR_SIZE)
            y_position = random.randint(STAR_SIZE, SCREEN_HEIGHT - STAR_SIZE)
            self.spawn_star(pg.Vector2(x_position, y_position))


    def spawn_stars(self):
        """Spawns a new star at the top of the screen."""
        x_position = random.randint(STAR_SIZE, SCREEN_WIDTH - STAR_SIZE)
        y_position = -STAR_SIZE
        self.spawn_star(pg.Vector2(x_position, y_position))

    # ------------------------------------------------------

    def init_game_objects(self):
        ship = Ship(self.units_sprites['ship.png'])
        self.ship = ship


    def load_all_images(self):
        self.units_sprites = self.load_images(UNIT_SPRITES_PATH)
        self.asteroids_sprites = self.load_images(ASTEROID_SPRITES_PATH)
        self.weapon_sprites = self.load_images(WEAPON_SPRITES_PATH)
        self.stars_sprites = self.load_images(STARS_SPRITES_PATH)


    def load_images(self, dir_path):
        sprite_dict = {}
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if file.endswith((".png", ".jpg", ".jpeg")):
                    path = os.path.join(root, file)
                    img = pg.image.load(path)
                    sprite_dict[file] = img
        return sprite_dict
    

    def init_time_variables(self):
        self.last_enemy_time = time.time()
        self.new_enemy_time = 3
        self.last_wave_time = time.time()
        self.new_wave_time = 10

        self.last_asteroid_spawn_time = time.time()
        self.asteroid_spawn_time = 3

        self.last_stars_spawn_time = time.time()
        self.stars_spawn_time = 0.2


    def spawn_time_objects(self, current_time):
        # check if it is time to spawn new wave of enemies
        if current_time - self.last_wave_time >= self.new_wave_time:
            print('New wave')
            self.last_wave_time = current_time
            self.enemy_type = BombEnemy

        # check if it is time to spawn a new enemy
        if current_time - self.last_enemy_time >= self.new_enemy_time:
            self.spawn_enemy()
            self.last_enemy_time = current_time

        # check if it is time to spawn a new background object
        if current_time - self.last_asteroid_spawn_time >= self.asteroid_spawn_time:
            self.spawn_asteroids()
            self.last_asteroid_spawn_time = current_time


        # check if it is time to spawn a new stars
        if current_time - self.last_stars_spawn_time >= self.stars_spawn_time:
            self.spawn_stars()
            self.last_stars_spawn_time = current_time