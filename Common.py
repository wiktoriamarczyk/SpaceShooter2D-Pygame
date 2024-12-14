import pygame as pg
import sys
from enum import Enum

DATA_PATH = 'data'
UNIT_SPRITES_PATH = 'data/sprites/units/'
WEAPON_SPRITES_PATH = 'data/sprites/weapons/'
ASTEROID_SPRITES_PATH = 'data/sprites/background/asteroids/'
STARS_SPRITES_PATH = 'data/sprites/background/stars/'

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (30, 30, 30)
STAR_COLORS = [(255,255,255), (239,234,232), (185, 217, 235), (174, 242, 231), (255, 186, 255), (187, 250, 223), (181, 195, 245)]
SHIP_SIZE = 64
STAR_SIZE = 16
ASTEROID_SIZE = 96

class EnemyTypes(Enum) :
    BASIC = 1
    SINUSOIDAL = 2
    DIAGONAL = 3
    ZIGZAG = 4

def are_floats_equal(a: float, b: float, tolerance: float = 1e-3) -> bool:
    return abs(a - b) <= tolerance