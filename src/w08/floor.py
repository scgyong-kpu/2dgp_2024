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
    def __init__(self, type, left, top):
        fname, (w, h) = INFO[type]
        x = left + w * UNIT // 2
        y = top + h * UNIT // 2
        super().__init__(fname, x, y)
        self.width = w * UNIT
        self.height = h * UNIT

    def draw(self):
        self.image.draw(self.x, self.y, self.width, self.height)

    def update(self):
        self.x += SPEED * gfw.frame_time
        if self.x < -self.width:
            world = gfw.top().world
            world.remove(self, world.layer.floor)

def init():
    global last_floor_right
    last_floor_right = 0
def draw():
    pass
def update():
    global last_floor_right
    last_floor_right += SPEED * gfw.frame_time
    # print(f'{last_floor_right=:.1f} {17*UNIT}')
    while last_floor_right < 17 * UNIT: # screen = 16x9 UNIT
        t = Floor.TYPE_20x2 if random.random() < 0.5 else Floor.TYPE_2x2
        f = Floor(t, last_floor_right, 0)
        # print(f'Appending {f} at f.left={f.x-f.width//2:.1f} {f.x=} {f.y=}')
        world = gfw.top().world
        world.append(f, world.layer.floor)
        last_floor_right += f.width
    # if random.random() < 0.01:
    #     world = gfw.top().world
    #     world.append(Floor(Floor.TYPE_3x1, 15, random.randint(3, 8)), world.layer.floor)

print(UNIT*16,UNIT*9)