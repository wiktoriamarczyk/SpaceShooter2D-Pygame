import os
import random
import time
from Common import *
from Ship import *
from Bullet import *
from BasicEnemy import *
from BombEnemy import *
from TargetingEnemey import TargetingEnemy
from BackgroundObject import *


class Engine:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Engine, cls).__new__(cls)
        return cls._instance

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
        self.__init_time_variables()

        # resources
        self.background = pg.image.load(BACKGROUND_PATH)
        self.scroll_x = 0
        self.scroll_y = 0
        self.background_x = 0

        self.units_sprites = []
        self.weapon_sprites = []
        self.asteroids_sprites = []
        self.stars_sprites = []
        self.__load_all_images()

        self.__spawn_init_stars()
        self.__init_game_objects()

    # ----------------- Public functions -----------------

    def run(self):
        while True:
            self.__handle_events()
            self.screen.fill(BACKGROUND_COLOR)
            self.clock.tick(self.frame_per_sec)
            delta_time = 1.0 / self.frame_per_sec
            self.__update(delta_time)
            self.__scroll_background()
            self.__render()
            # update the display
            pg.display.flip()


    def get_ship_position(self):
        return self.ship.position
    

    def get_bullet_texture(self, texture_name):
        return self.weapon_sprites[texture_name]
    

    def add_object(self, game_object):
        self.game_objects.append(game_object)

    # ----------------- Main functions -----------------

    def __handle_events(self):
        for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYUP:
                     if event.key == pg.K_SPACE:
                        self.__fire_bullet()


    def __render(self):
        for game_object in self.game_objects:
            game_object.render(self.screen)
        self.ship.render(self.screen)


    def __update(self, delta_time):
        current_time = time.time()

        # remove dead game objects
        for go in self.game_objects:
            if go.alive == False:
                self.game_objects.remove(go)
                go.__del__()

        self.__spawn_time_objects(current_time)

        for game_object in self.game_objects:
            game_object.update(delta_time)
        self.ship.update(delta_time)


    def __scroll_background(self):
        # Scroll the background horizontally
        self.scroll_y += 1
        
        # Draw the background twice to create seamless scrolling effect
        self.screen.blit(self.background, (self.scroll_x, self.scroll_y))
        self.screen.blit(self.background, (self.scroll_x, self.scroll_y - self.background.get_height()))

        # Reset the background position when it goes off screen
        if self.scroll_y >= self.background.get_height():
            self.scroll_y = 0

    
    # ------------------------------------------------------

    # ----------------- Game objects management -----------------

    def __init_game_objects(self):
        ship = Ship(self.units_sprites['ship.png'])
        self.ship = ship


    def __fire_bullet(self):
        bullet_pos = self.ship.position
        bullet = Bullet(pg.Vector2(bullet_pos.x + 5, bullet_pos.y - 10), self.weapon_sprites['bullet.png'])
        self.game_objects.append(bullet)


    def __spawn_enemy(self):
        x_position = random.randint(2*SHIP_SIZE, SCREEN_WIDTH - 2*SHIP_SIZE)
        
        sprite_path = "bullet-ship.png"
        if self.enemy_type == BombEnemy:
            sprite_path = "bomb-ship.png"
        elif self.enemy_type == TargetingEnemy:
            sprite_path = "targeting-ship.png"

        enemy = self.enemy_type(pg.Vector2(x_position, -SHIP_SIZE), self.units_sprites[sprite_path])
        self.game_objects.append(enemy)

    # ------------------------------------------------------

    # ----------------- Background objects -----------------

    def __spawn_background_object(self, sprite_list, position, size_range, depth_range, color=None):
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


    def __spawn_asteroids(self):
        """Spawns an asteroid."""
        size_range = (ASTEROID_MIN_SIZE, ASTEROID_MAX_SIZE)
        depth_range = (1, 2)
        x_position = random.randint(2 * size_range[1], SCREEN_WIDTH - 2 * size_range[1])
        position = pg.Vector2(x_position, -size_range[1])
        self.__spawn_background_object(self.asteroids_sprites, position, size_range, depth_range)


    def __spawn_star(self, position):
        """Spawns a single star at the specified position."""
        color=None
        rand_color = random.randint(1, 4)

        if rand_color == 1:
            color = random.choice(STAR_COLORS)
        size_range = (STAR_MIN_SIZE, STAR_MAX_SIZE)
        depth_range = (1, 2)
        self.__spawn_background_object(self.stars_sprites, position, size_range, depth_range, color)


    def __spawn_init_stars(self):
        """Spawns initial stars randomly across the screen."""
        for _ in range(25):
            x_position = random.randint(STAR_MAX_SIZE, SCREEN_WIDTH - STAR_MAX_SIZE)
            y_position = random.randint(STAR_MAX_SIZE, SCREEN_HEIGHT - STAR_MAX_SIZE)
            self.__spawn_star(pg.Vector2(x_position, y_position))


    def __spawn_stars(self):
        """Spawns a new star at the top of the screen."""
        x_position = random.randint(STAR_MAX_SIZE, SCREEN_WIDTH - STAR_MAX_SIZE)
        y_position = -STAR_MAX_SIZE
        self.__spawn_star(pg.Vector2(x_position, y_position))

    # ------------------------------------------------------

    # ----------------- Resource loading -----------------

    def __load_all_images(self):
        self.units_sprites = self.__load_images(UNIT_SPRITES_PATH)
        self.asteroids_sprites = self.__load_images(ASTEROID_SPRITES_PATH)
        self.weapon_sprites = self.__load_images(WEAPON_SPRITES_PATH)
        self.stars_sprites = self.__load_images(STARS_SPRITES_PATH)


    def __load_images(self, dir_path):
        sprite_dict = {}
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if file.endswith((".png", ".jpg", ".jpeg")):
                    path = os.path.join(root, file)
                    img = pg.image.load(path)
                    sprite_dict[file] = img
        return sprite_dict
    
    # ------------------------------------------------------
        
    # ----------------- Time objects management -----------------

    def __init_time_variables(self):
        self.last_enemy_time = time.time()
        self.new_enemy_time = 2

        self.last_wave_time = time.time()
        self.new_wave_time = 6

        self.last_asteroid_spawn_time = time.time()
        self.asteroid_spawn_time = 3

        self.last_stars_spawn_time = time.time()
        self.stars_spawn_time = 0.2


    def __spawn_time_objects(self, current_time):
        # check if it is time to spawn new wave of enemies
        if current_time - self.last_wave_time >= self.new_wave_time:
            self.last_wave_time = current_time
            if self.enemy_type == BombEnemy:
                self.enemy_type = TargetingEnemy
            else:
                self.enemy_type = BombEnemy


        # check if it is time to spawn a new enemy
        if current_time - self.last_enemy_time >= self.new_enemy_time:
            self.__spawn_enemy()
            self.last_enemy_time = current_time

        # check if it is time to spawn a new background object
        if current_time - self.last_asteroid_spawn_time >= self.asteroid_spawn_time:
            self.__spawn_asteroids()
            self.last_asteroid_spawn_time = current_time

        # check if it is time to spawn stars
        if current_time - self.last_stars_spawn_time >= self.stars_spawn_time:
            self.__spawn_stars()
            self.last_stars_spawn_time = current_time

    # ------------------------------------------------------