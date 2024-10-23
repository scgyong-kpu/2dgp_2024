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

class MapObject(Sprite):
    def __init__(self, fname, left, top, unit_width, unit_height):
        x = left + unit_width * UNIT // 2
        y = top + unit_height * UNIT // 2
        super().__init__(fname, x, y)
        self.width = unit_width * UNIT
        self.height = unit_height * UNIT

    def draw(self):
        self.image.draw(self.x, self.y, self.width, self.height)

    def update(self):
        self.x += SPEED * gfw.frame_time
        if self.x < -self.width:
            world = gfw.top().world
            world.remove(self)

class Floor(MapObject):
    TYPE_20x2, TYPE_2x2, TYPE_3x1 = range(3)
    def __init__(self, type, left, top):
        fname, (w, h) = INFO[type]
        super().__init__(fname, left, top, w, h)
        self.layer_index = gfw.top().world.layer.floor


class JellyItem(MapObject):
    def __init__(self, index, left, top):
        super().__init__('res/jelly.png', left, top, 1, 1)
        x = round(2 + (index  % 30) * 68)
        y = round(2 + (index // 30) * 68)
        self.src_rect = x, y, 66, 66
        self.width, self.height = 48, 48
        self.layer_index = gfw.top().world.layer.item

    def draw(self):
        self.image.clip_draw(*self.src_rect, self.x, self.y)

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
        world.append(f)

        jelly = JellyItem(random.randrange(60), last_floor_right, random.randint(3,8)*UNIT)
        # print(f'Appending {jelly} at jelly.left={jelly.x-jelly.width//2:.1f} {jelly.x=:.1f} {jelly.y=}')
        world.append(jelly)

        last_floor_right += f.width
    # if random.random() < 0.01:
    #     world = gfw.top().world
    #     world.append(Floor(Floor.TYPE_3x1, 15, random.randint(3, 8)), world.layer.floor)

