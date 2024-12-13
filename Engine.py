import os
import random
import time
from Common import *
from Ship import *
from Bullet import *
from BasicEnemy import *
from BombEnemy import *

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
        self.last_enemy_spawn_time = time.time()
        self.new_wave_spawn_time = 10
        self.last_wave_time = time.time()

        self.images = self.load_images()

        self.initialize_game_objects()


    def run(self):
        while True:
            self.handle_events()
            self.screen.fill(BACKGROUND_COLOR)
            self.clock.tick(self.frame_per_sec)
            delta_time = 1.0 / self.frame_per_sec
            self.update(delta_time)
            self.render()
            # Update the display
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


    def update(self, delta_time):
        # remove dead game objects
        for go in self.game_objects:
            if go.alive == False:
                self.game_objects.remove(go)
                go.__del__()

        current_time = time.time()

        # check if it is time to spawn new wave of enemies
        if current_time - self.last_wave_time >= self.new_wave_spawn_time:
            print('New wave')
            self.last_wave_time = current_time
            self.enemy_type = BombEnemy

        # check if it is time to spawn a new enemy
        if current_time - self.last_enemy_spawn_time >= 3:
            self.spawn_enemy()
            self.last_enemy_spawn_time = current_time

        for game_object in self.game_objects:
            game_object.update(delta_time)


    def fire_bullet(self):
        bullet_pos = self.ship.position
        bullet = Bullet(pg.Vector2(bullet_pos.x + 5, bullet_pos.y - 10), self.images['bullet.png'])
        self.game_objects.append(bullet)


    def spawn_enemy(self):
        x_position = random.randint(2*SHIP_SIZE, SCREEN_WIDTH - 2*SHIP_SIZE)
        
        sprite_path = "bullet-ship.png"
        if self.enemy_type == BombEnemy:
            sprite_path = "bomb-ship.png"

        enemy = self.enemy_type(pg.Vector2(x_position, -SHIP_SIZE), self.images[sprite_path])
        self.game_objects.append(enemy)


    def initialize_game_objects(self):
        ship = Ship(self.images['ship.png'])
        self.ship = ship
        self.game_objects.append(ship)


    # load all images from all subdirectories
    def load_images(self):
        path = DATA_PATH
        images = {}
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith('.png'):
                    image = pg.image.load(os.path.join(root, file))
                    images[file] = image
        return images