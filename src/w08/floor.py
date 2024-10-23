from pico2d import * 
from gfw import *

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
    world.append(Floor(Floor.TYPE_20x2, 0, 0), world.layer.floor)
    world.append(Floor(Floor.TYPE_2x2, 20, 0), world.layer.floor)
    world.append(Floor(Floor.TYPE_3x1, 5, 4), world.layer.floor)

def draw():
    pass
def update():
    pass
