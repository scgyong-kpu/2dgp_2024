from pico2d import * 
from gfw import *
import random

INFO = [
    ('res/cookierun_platform_480x48.png', (20, 2)),
    ('res/cookierun_platform_124x120.png', (2, 2)),
    ('res/cookierun_platform_120x40.png', (3, 1)),
]
UNIT = 72
SPEED = -300

class Floor(Sprite):
    TYPE_20x2, TYPE_2x2, TYPE_3x1 = range(3)
    def __init__(self, type, left_unit, top_unit):
        fname, (w, h) = INFO[type]
        x = left_unit * UNIT + w * UNIT // 2
        y = top_unit * UNIT + h * UNIT // 2
        super().__init__(fname, x, y)
        self.width = w * UNIT
        self.height = h * UNIT

    def draw(self):
        self.image.draw(self.x, self.y, self.width, self.height)

    def update(self):
        self.x += SPEED * gfw.frame_time

def init():
    world = gfw.top().world
    x = 0
    while x < 1000:
        t = Floor.TYPE_20x2 if random.random() < 0.5 else Floor.TYPE_2x2
        w = 20 if t == Floor.TYPE_20x2 else 2
        world.append(Floor(t, x, 0), world.layer.floor)
        x += w

def draw():
    pass
def update():
    if random.random() < 0.01:
        world = gfw.top().world
        world.append(Floor(Floor.TYPE_3x1, 15, random.randint(3, 8)), world.layer.floor)
