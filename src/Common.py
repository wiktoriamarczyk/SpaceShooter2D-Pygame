import pygame as pg
from enum import Enum
import os

base_path = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(base_path, '../data')
SPRITES_PATH = os.path.join(DATA_PATH, 'sprites')
BACKGROUND_PATH = os.path.join(SPRITES_PATH, 'background', 'background.png')
ASTEROIDS_PATH = os.path.join(SPRITES_PATH, 'background', 'asteroids')
STARS_PATH = os.path.join(SPRITES_PATH, 'background', 'stars')
UNITS_PATH = os.path.join(SPRITES_PATH, 'units')
WEAPONS_PATH = os.path.join(SPRITES_PATH, 'weapons')
POWER_UPS_PATH = os.path.join(SPRITES_PATH, 'power-ups')

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (30, 30, 30)
STAR_COLORS = [(255,255,255), (238,116,17), (77,194,145), (227,220,82)]
SHIP_SIZE = 64
BULLET_SIZE = 16
BOMB_SIZE = POWER_UP_SIZE = 32
BOSS_SIZE = 128

STAR_MIN_SIZE = 12
STAR_MAX_SIZE = 18
ASTEROID_MIN_SIZE = 64
ASTEROID_MAX_SIZE = 96

COLLISION_DEALT_DAMAGE = 2
HEALTH_POWER_UP_AMOUNT = 250
SHIELD_POWER_UP_TIME = 3

DEFAULT_FONT_NAME = "Consolas"
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
RECT_DEFAULT_COLOR = (32, 32, 32)

class EnemySprites(Enum) :
    BasicEnemy = UNITS_PATH + "/bullet-ship.png"
    BombEnemy = UNITS_PATH + "/bomb-ship.png"
    TargetingEnemy = UNITS_PATH + "/targeting-ship.png"

class EnemyTypes(Enum) :
    BasicEnemy = 0
    BombEnemy = 1
    TargetingEnemy = 2

ENEMY_TYPE_TO_SPRITE = {
    EnemyTypes.BasicEnemy: EnemySprites.BasicEnemy,
    EnemyTypes.BombEnemy: EnemySprites.BombEnemy,
    EnemyTypes.TargetingEnemy: EnemySprites.TargetingEnemy
}

class ObjectDirection(Enum) :
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class GameStateID(Enum) :
    UNKNOWN = 0
    MAIN_MENU = 1
    GAME = 2
    GAME_OVER = 3

class PowerUpTypes(Enum) :
    HEALTH = 0
    SHIELD = 1

def are_floats_equal(a: float, b: float, tolerance: float = 1e-3) -> bool:
    return abs(a - b) <= tolerance