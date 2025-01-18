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
from PowerUp import PowerUp
from Boss import Boss

class InGameState (GameState):
    def __init__(self, ID):
        super().__init__(ID)
        self.next_state = GameStateID.GAME_OVER

        self.game_objects = []
        self.ship = None
        self.enemy_types = [BasicEnemy, BombEnemy, TargetingEnemy]
        self.enemy_type_index = 0
        self.enemy_wave_index = 1
        self.boss = None
        self.enemies_defeated = 0
        self.total_enemies_spawned = 0
        self.total_enemies_to_spawn = 15

        self.powerup_health_path = os.path.join(POWER_UPS_PATH, "first-aid-kit.png")
        self.powerup_shield_path = os.path.join(POWER_UPS_PATH, "shield.png")
        self.bullet_path = os.path.join(WEAPONS_PATH, "rocket0.png")
        self.boss_path = os.path.join(UNITS_PATH, "boss.png")
        self.ship_path = os.path.join(UNITS_PATH, "ship.png")

        pg.font.init()
        self.__init_game_objects()
        self.__init_time_variables()


    def update(self, delta_time):
        current_time = time.time()

        # remove dead game objects
        for go in self.game_objects:
            if go.alive == False:
                if isinstance(go, Enemy) and go.death_by_time == True:
                    self.enemies_defeated += 1
                    from Engine import Engine
                    Engine._instance.add_points(1)
                self.game_objects.remove(go)

        self.__check_collisions()
        self.__spawn_time_objects(current_time)

        # update game objects
        for game_object in self.game_objects:
            game_object.update(delta_time)
        self.ship.update(delta_time)


    def render(self, screen):
        for game_object in self.game_objects:
            game_object.render(screen)

        self.ship.render(screen)
        self.__render_points(screen)


    def handle_events(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.__fire_bullet()


    def add_object(self, game_object):
        self.game_objects.append(game_object)
    

    def get_ship_position(self):
        return self.ship.position
    

    def __render_points(self, screen):
        font = pg.font.SysFont("Consolas", 20)
        text = font.render("Defeated: " + str(self.enemies_defeated) + "/" + str(self.total_enemies_to_spawn), True, COLOR_WHITE)
        screen.blit(text, (10, 35))


    def __init_game_objects(self):
        from Engine import Engine
        sprite = Engine._instance.get_sprite(self.ship_path)     
        ship = Ship(sprite)
        self.ship = ship


    def __fire_bullet(self):
        bullet_pos = self.ship.position

        from Engine import Engine
        sprite = Engine._instance.get_sprite(self.bullet_path)  
        
        bullet = Bullet(pg.Vector2(bullet_pos.x + 5, bullet_pos.y - 10), sprite)
        bullet.set_ownership(True)
        bullet.set_dealing_damage(20)
        self.game_objects.append(bullet)


    def __spawn_enemy(self):
        self.total_enemies_spawned += 1

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


    def __spawn_boss(self):
        from Engine import Engine
        boss_sprite = Engine._instance.get_sprite(self.boss_path)
        self.boss = Boss(pg.Vector2(SCREEN_WIDTH / 2, -BOSS_SIZE), boss_sprite)
        self.game_objects.append(self.boss)


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

            if isinstance(go, PowerUp):
                if self.__check_rect_collision(go, self.ship) == True:
                    if go.type == PowerUpTypes.HEALTH:
                        self.ship.update_health(HEALTH_POWER_UP_AMOUNT)
                    elif go.type == PowerUpTypes.SHIELD:
                        self.ship.activate_shield_defense(SHIELD_POWER_UP_TIME)

                    self.game_objects.remove(go)

        # check ship collision with enemy bullets
        for eb in enemy_bullets:
            if self.__check_rect_collision(eb, self.ship) == True:
                self.ship.update_health(-eb.dealing_damage)
                if eb.dead_by_collision == True:
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
       

    # TODO: change this to a random floats
    def __init_time_variables(self):
        self.last_enemy_time = time.time()
        self.new_enemy_time = random.randint(1, 3)

        self.last_wave_time = time.time()
        self.new_wave_time = random.randint(5, 8)

        self.last_power_up_time = time.time()
        self.new_power_up_time = random.randint(4, 8)


    def __spawn_time_objects(self, current_time):
        # check if it is time to spawn a new power up
        if current_time - self.last_power_up_time >= self.new_power_up_time:
            self.last_power_up_time = current_time
            
            pos = random.randint(0, 1)
            if pos == 0:
                direction = ObjectDirection.RIGHT
                position_x = POWER_UP_SIZE
            else:
                direction = ObjectDirection.LEFT
                position_x = SCREEN_WIDTH + POWER_UP_SIZE

            position_y = random.randrange(2*POWER_UP_SIZE, 8*POWER_UP_SIZE, 10)

            type_rand = random.randint(0, 1)
            if type_rand == 0:
                type = PowerUpTypes.HEALTH
                from Engine import Engine
                sprite = Engine._instance.get_sprite(self.powerup_health_path)
            else:
                type = PowerUpTypes.SHIELD
                from Engine import Engine
                sprite = Engine._instance.get_sprite(self.powerup_shield_path)

            power_up = PowerUp(pg.Vector2(position_x, position_y), sprite, direction, type)
            self.game_objects.append(power_up)
                

        # check if it is time to spawn the boss
        if self.total_enemies_spawned == self.total_enemies_to_spawn and self.boss is None:
            self.__spawn_boss()
            return
        
        if self.total_enemies_spawned == self.total_enemies_to_spawn:
            return

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