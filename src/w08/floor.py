from pico2d import * 
from gfw import *
import random
import json

INFO = [
    ('res/cookierun_platform_480x48.png', (10, 2)),
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
    TYPE_10x2, TYPE_2x2, TYPE_3x1 = range(3)
    def __init__(self, type, left, top):
        fname, (w, h) = INFO[type]
        super().__init__(fname, left, top, w, h)
        self.layer_index = gfw.top().world.layer.floor


class JellyItem(MapObject):
    def __init__(self, index, left, top):
        super().__init__('res/jelly.png', left, top, 1, 1)
        x = round(2 + (index  % 30) * 68)
        y = round(2 + (1 - index // 30) * 68)
        self.src_rect = x, y, 66, 66
        self.width, self.height = 48, 48
        self.layer_index = gfw.top().world.layer.item

    def draw(self):
        self.image.clip_draw(*self.src_rect, self.x, self.y)

def mapobject_factory_create(tile, left, bottom):
    if tile >= 1 and tile <= 60:
        return JellyItem(tile - 1, left, bottom)
    if tile == 91 or tile == 101 or tile == 73:
        type = Floor.TYPE_10x2 if tile == 91 else Floor.TYPE_2x2 if tile == 101 else Floor.TYPE_3x1
        return Floor(type, left, bottom)
    return None

def init():
    with open('res/stage_01.tmj') as f:
        tmj = json.load(f)
        # print(tmj)

    global map_width, map_height, map_data
    global last_floor_right, map_x
    world = gfw.top().world
    map_width = tmj['width']
    map_height = tmj['height']
    map_data = tmj['layers'][0]['data']
    last_floor_right = 0
    map_x = 0
def draw():
    pass
def update():
    global last_floor_right, map_x

    last_floor_right += SPEED * gfw.frame_time

    while last_floor_right < 17 * UNIT:
        bottom = 0
        for y in range(map_height - 1, -1, -1):
            tile = map_data[y * map_width + map_x]
            obj = mapobject_factory_create(tile, last_floor_right, bottom)
            if obj is not None:
                # print(f'@({map_x}, {y}) {obj} ({obj.x},{obj.y}) [{obj.x - obj.width//2} ~ {obj.x + obj.width//2}]')
                world = gfw.top().world
                world.append(obj)
            bottom += UNIT
        map_x += 1
        last_floor_right += UNIT
        print(f'{map_x=} / {map_width=}')

