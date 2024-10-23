from pico2d import * 
from gfw import *

FILENAMES = [
    'res/cookierun_platform_480x48.png',
    'res/cookierun_platform_124x120.png',
    'res/cookierun_platform_120x40.png',
]

class Floor(Sprite):
    TYPE_20x2, TYPE_2x2, TYPE_3x1 = range(3)
    def __init__(self, type, x, y):
        super().__init__(FILENAMES[type], x, y)



