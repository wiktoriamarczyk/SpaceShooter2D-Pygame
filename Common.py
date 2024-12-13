import pygame as pg
import sys
from enum import Enum

DATA_PATH = 'data'
UNIT_SPRITES_PATH = 'data/sprites/units/'
WEAPON_SPRITES_PATH = 'data/sprites/weapons/'
BACKGROUND_SPRITES_PATH = 'data/sprites/background/'

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (30, 30, 30)
SHIP_SIZE = 64

class EnemyTypes(Enum) :
    BASIC = 1
    SINUSOIDAL = 2
    DIAGONAL = 3
    ZIGZAG = 4

def are_floats_equal(a: float, b: float, tolerance: float = 1e-3) -> bool:
    return abs(a - b) <= tolerance