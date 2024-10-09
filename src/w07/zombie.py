import random
from pico2d import *
from gfw import *

class Zombie(AnimSprite):
    FPS = 8
    def __init__(self):
        x, y = random.randrange(get_canvas_width()), random.randrange(get_canvas_height())
        super().__init__('res/zombiefiles/male/Idle (1).png', x, y, self.FPS, 1)
