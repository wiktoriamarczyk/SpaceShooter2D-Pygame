import pygame as pg
import sys
from enum import Enum

DATA_PATH = 'data'
UNIT_SPRITES_PATH = 'data/sprites/units/'
WEAPON_SPRITES_PATH = 'data/sprites/weapons/'
ASTEROID_SPRITES_PATH = 'data/sprites/background/asteroids/'
STARS_SPRITES_PATH = 'data/sprites/background/stars/'
BACKGROUND_PATH = 'data/sprites/background/background.png'

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (30, 30, 30)
STAR_COLORS = [(255,255,255), (238,116,17), (77,194,145), (227,220,82)]
SHIP_SIZE = 64
BULLET_SIZE = 16

STAR_MIN_SIZE = 12
STAR_MAX_SIZE = 18
ASTEROID_MIN_SIZE = 64
ASTEROID_MAX_SIZE = 96

class EnemyTypes(Enum) :
    BASIC = 1
    SINUSOIDAL = 2
    DIAGONAL = 3
    ZIGZAG = 4

class ObjectDirection(Enum) :
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

def are_floats_equal(a: float, b: float, tolerance: float = 1e-3) -> bool:
    return abs(a - b) <= tolerance