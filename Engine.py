import os
import random
import time
from Common import *
from Ship import *
from Bullet import *
from BasicEnemy import *
from BombEnemy import *
from TargetingEnemy import TargetingEnemy
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
        self.enemy_types = [BasicEnemy, BombEnemy, TargetingEnemy]
        self.enemy_type_index = 0

        # time variables
        self.__init_time_variables()

        # resources
        self.background = pg.image.load(BACKGROUND_PATH)
        self.scroll_x = 0
        self.scroll_y = 0
        self.background_x = 0

        self.sprites = []
        self.stars_sprites = []
        self.asteroids_sprites = []

        self.__load_images(self.stars_sprites, STARS_PATH)
        self.__load_images(self.asteroids_sprites, ASTEROIDS_PATH)
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
    

    def get_sprite(self, sprite_name):
        # find the sprite
        if sprite_name in self.sprites:
            return self.sprites[self.sprites.index(sprite_name)]
        # else load the sprite
        sprite = pg.image.load(sprite_name)
        if sprite is None:
            return None
        self.sprites.append(sprite)
        return sprite

    
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

        self.__check_collisions()

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
        path = UNITS_PATH + "/ship.png"
        sprite = self.get_sprite(path)
        ship = Ship(sprite)
        self.ship = ship


    def __fire_bullet(self):
        bullet_pos = self.ship.position
        path = WEAPONS_PATH + "/bullet.png"
        sprite = self.get_sprite(path)
        bullet = Bullet(pg.Vector2(bullet_pos.x + 5, bullet_pos.y - 10), sprite)
        bullet.set_ownership(True)
        bullet.set_dealing_damage(20)
        self.game_objects.append(bullet)


    def __spawn_enemy(self):
        x_position = random.randint(2*SHIP_SIZE, SCREEN_WIDTH - 2*SHIP_SIZE)
        
        enemy_type = EnemyTypes(self.enemy_type_index)
        sprite_path = ENEMY_TYPE_TO_SPRITE[enemy_type].value
        sprite = self.get_sprite(sprite_path)
        if sprite is None:
            return
        enemy_class = self.enemy_types[self.enemy_type_index]
        enemy = enemy_class(pg.Vector2(x_position, -SHIP_SIZE), sprite)
        self.game_objects.append(enemy)


    def __check_rect_collision(self, go1, go2):
        if isinstance(go1, GameObject) and isinstance(go2, GameObject):
            return go1.get_rect().colliderect(go2.get_rect())
        return False
    

    # TO FIX: Make sure to check the collision only once
    def __check_collisions(self):

        player_bullets = []
        enemy_bullets = []

        for go in self.game_objects:
            if isinstance(go, Weapon):
                if go.is_owned_by_player == True:
                    player_bullets.append(go)
                else:
                    enemy_bullets.append(go)

        # check ship collision with enemy bullets
        for eb in enemy_bullets:
            if self.__check_rect_collision(eb, self.ship) == True:
                self.ship.update_health(eb.dealing_damage)
                eb.clear_health()

        for go in self.game_objects:
            # for each enemy
            if isinstance(go, Enemy):
                # check collision with player ship
                if self.__check_rect_collision(go, self.ship) == True:
                    self.ship.update_health(COLLISION_DEALT_DAMAGE)
                    go.update_health(COLLISION_DEALT_DAMAGE)
                    print("Ship health: ", go.health)
                # check collision with player bullets
                for pb in player_bullets:
                    if self.__check_rect_collision(go, pb) == True:
                        go.update_health(pb.dealing_damage)
                        pb.clear_health()
       

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
        sprite_image = random.choice(sprite_list)
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

    def __load_images(self, array, dir_path):
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if file.endswith((".png", ".jpg", ".jpeg")):
                    path = os.path.join(root, file)
                    img = pg.image.load(path)
                    array.append(img)

    
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
            self.enemy_type_index = (self.enemy_type_index + 1) % len(self.enemy_types)

        # check if it is time to spawn a new enemy from the wave
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