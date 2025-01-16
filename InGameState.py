import random
import time

from Common import *

from GameObject import GameObject
from GameState import GameState
from Enemy import Enemy
from Ship import Ship
from Bullet import Bullet
from BasicEnemy import BasicEnemy
from BombEnemy import BombEnemy
from TargetingEnemy import TargetingEnemy
from Weapon import Weapon

class InGameState (GameState):
    def __init__(self, ID):
        super().__init__(ID)

        # units
        self.game_objects = []
        self.ship = None
        self.enemy_types = [BasicEnemy, BombEnemy, TargetingEnemy]
        self.enemy_type_index = 0
        self.enemy_wave_index = 1

        self.__init_game_objects()

        # time variables
        self.__init_time_variables()


    def update(self, delta_time):
        current_time = time.time()

        # remove dead game objects
        for go in self.game_objects:
            if go.alive == False:
                self.game_objects.remove(go)

        # check collisions
        self.__check_collisions()

        self.__spawn_time_objects(current_time)

        # update game objects
        for game_object in self.game_objects:
            game_object.update(delta_time)
        self.ship.update(delta_time)


    def render(self, screen):
        # render game objects
        for game_object in self.game_objects:
            game_object.render(screen)
        self.ship.render(screen)
        self.__render_health_bars(screen)


    def handle_events(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.__fire_bullet()


    def __init_game_objects(self):
        path = UNITS_PATH + "/ship.png"

        from Engine import Engine
        sprite = Engine._instance.get_sprite(path)     
        ship = Ship(sprite)
        self.ship = ship

    
    def __render_health_bars(self, screen):
        # Dimensions of the health bar
        player_bar_width = 200
        player_bar_height = 20
        enemy_bar_witdh = 50
        enemy_bar_height = 10
        player_bar_x = 10  # Padding from the left
        player_bar_y = 10  # Padding from the top

        # Draw health bar for Player
        health_percentage = max(0, self.ship.health / self.ship.max_health)
        current_bar_width = int(player_bar_width * health_percentage)

        pg.draw.rect(screen, (100, 100, 100), (player_bar_x, player_bar_y, player_bar_width, player_bar_height))  # Background
        pg.draw.rect(screen, (0, 255, 0), (player_bar_x, player_bar_y, current_bar_width, player_bar_height))  # Foreground
        pg.draw.rect(screen, (255, 255, 255), (player_bar_x, player_bar_y, player_bar_width, player_bar_height), 2) # Border

        # Draw health bar for Enemies
        for go in self.game_objects:
            if isinstance(go, Enemy):
                health_percentage = max(0, go.health / go.max_health)
                current_bar_width = int(enemy_bar_witdh * health_percentage)

                enemy_bar_x = int(go.position.x - enemy_bar_witdh / 2)
                enemy_bar_y = int(go.position.y - SHIP_SIZE / 2 - 10)

                pg.draw.rect(screen, (100, 100, 100), (enemy_bar_x, enemy_bar_y, enemy_bar_witdh, enemy_bar_height))
                pg.draw.rect(screen, (0, 255, 0), (enemy_bar_x, enemy_bar_y, current_bar_width, enemy_bar_height))
                pg.draw.rect(screen, (255, 255, 255), (enemy_bar_x, enemy_bar_y, enemy_bar_witdh, enemy_bar_height), 2)


    def __fire_bullet(self):
        bullet_pos = self.ship.position
        path = WEAPONS_PATH + "/bullet.png"

        from Engine import Engine
        sprite = Engine._instance.get_sprite(path)   
        
        bullet = Bullet(pg.Vector2(bullet_pos.x + 5, bullet_pos.y - 10), sprite)
        bullet.set_ownership(True)
        bullet.set_dealing_damage(20)
        self.game_objects.append(bullet)


    def __spawn_enemy(self):
        x_position = random.randint(2*SHIP_SIZE, SCREEN_WIDTH - 2*SHIP_SIZE)
        
        enemy_type = EnemyTypes(self.enemy_type_index)
        sprite_path = ENEMY_TYPE_TO_SPRITE[enemy_type].value
        
        from Engine import Engine
        sprite = Engine._instance.get_sprite(sprite_path)  
        if sprite is None:
            return
        
        enemy_class = self.enemy_types[self.enemy_type_index]
        enemy = enemy_class(pg.Vector2(x_position, -SHIP_SIZE), sprite)
        self.game_objects.append(enemy)


    def __check_rect_collision(self, go1, go2):
        if isinstance(go1, GameObject) and isinstance(go2, GameObject):
            return go1.get_rect().colliderect(go2.get_rect())
        return False


    def get_next_state_ID(self):
        return GameStateID.MAIN_MENU


    def add_object(self, game_object):
        self.game_objects.append(game_object)
    

    def get_ship_position(self):
        return self.ship.position
    

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
                self.ship.update_health(-eb.dealing_damage)
                eb.clear_health()

        for go in self.game_objects:
            # for each enemy
            if isinstance(go, Enemy):
                # check collision with player ship
                if self.__check_rect_collision(go, self.ship) == True:
                    self.ship.update_health(-COLLISION_DEALT_DAMAGE)
                    go.update_health(-COLLISION_DEALT_DAMAGE)
                # check collision with player bullets
                for pb in player_bullets:
                    if self.__check_rect_collision(go, pb) == True:
                        go.update_health(-pb.dealing_damage)
                        pb.clear_health()
       

    def __init_time_variables(self):
        self.last_enemy_time = time.time()
        self.new_enemy_time = random.randint(1, 3)

        self.last_wave_time = time.time()
        self.new_wave_time = random.randint(3, 8)


    def __spawn_time_objects(self, current_time):
        # check if it is time to spawn new wave of enemies
        if current_time - self.last_wave_time >= self.new_wave_time:
            self.enemy_wave_index += 1
            self.last_wave_time = current_time

            # if we have spawned all enemy waves, spawn random enemy wave
            if self.enemy_wave_index > len(self.enemy_types):
                self.enemy_type_index = random.randint(0, len(self.enemy_types) - 1)
            else:
                self.enemy_type_index = (self.enemy_type_index + 1) % len(self.enemy_types)

        # check if it is time to spawn a new enemy from the wave
        if current_time - self.last_enemy_time >= self.new_enemy_time:
            self.__spawn_enemy()
            self.last_enemy_time = current_time