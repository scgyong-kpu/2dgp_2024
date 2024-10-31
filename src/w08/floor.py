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
lines = []

class MapObject(Sprite):
    def __init__(self, fname, left, bottom, unit_width, unit_height):
        x = left + unit_width * UNIT // 2
        y = bottom + unit_height * UNIT // 2
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
    def __init__(self, type, left, bottom):
        fname, (w, h) = INFO[type]
        super().__init__(fname, left, bottom, w, h)
        self.type = type
        self.layer_index = gfw.top().world.layer.floor
    def canPassThrough(self):
        return not self.type in (Floor.TYPE_10x2, Floor.TYPE_2x2)

class JellyItem(MapObject):
    def __init__(self, index, left, bottom):
        super().__init__('res/jelly.png', left, bottom, 1, 1)
        x = round(2 + (index  % 30) * 68)
        y = round(2 + (1 - index // 30) * 68)
        self.src_rect = x, y, 66, 66
        self.width, self.height = 48, 48
        self.layer_index = gfw.top().world.layer.item

    def draw(self):
        self.image.clip_draw(*self.src_rect, self.x, self.y)

class Obstacle(MapObject):
    def __init__(self, fname, left, bottom):
        super().__init__(fname, left, bottom, 1, 1)
        self.width = self.image.w
        bottom = self.y + self.height / 2
        self.height = self.image.h
        self.y = bottom + self.height / 2

        self.layer_index = gfw.top().world.layer.obstacle

    def get_bb(self):
        foot = self.y - self.height // 2
        (bb_size, _) = self.info
        bb_half_width = self.width * bb_size[0] / 2
        bb_height = self.height * bb_size[1]
        return (self.x - bb_half_width, foot, self.x + bb_half_width, foot + bb_height)


class SimpleObstacle(Obstacle):
    def __init__(self, left, bottom):
        super().__init__('res/witchs_oven/epN01_tm01_jp1A.png', left, bottom)
        self.info = ( (0.5, 0.8), [] )

ANIM_OBSTACLE_INFO = [
    ( (0.7, 0.5), [
        'res/witchs_oven/epN01_tm01_jp1up_01.png',
        'res/witchs_oven/epN01_tm01_jp1up_02.png',
        'res/witchs_oven/epN01_tm01_jp1up_03.png',
        'res/witchs_oven/epN01_tm01_jp1up_04.png',
    ] ),
    ( (0.7, 0.6), [
        'res/witchs_oven/epN01_tm01_jp2up_01.png',
        'res/witchs_oven/epN01_tm01_jp2up_02.png',
        'res/witchs_oven/epN01_tm01_jp2up_03.png',
        'res/witchs_oven/epN01_tm01_jp2up_04.png',
        'res/witchs_oven/epN01_tm01_jp2up_05.png',
    ] ),
]

class AnimObstacle(Obstacle):
    def __init__(self, info, left, bottom):
        (_, files) = info
        super().__init__(files[0], left, bottom)
        self.info = info
        self.images = list(map(gfw.image.load, files))
        self.fps = 6
        self.frame_count = len(self.images)
        self.time = 0

    def update(self):
        super().update()
        if (self.x < get_canvas_width() * 3 // 4):
            self.time += gfw.frame_time

    def draw(self):
        index = round(self.time * self.fps)
        if index >= len(self.images): index = len(self.images) - 1
        self.images[index].draw(self.x, self.y, self.width, self.height)

def mapobject_factory_create(tile, left, bottom):
    if tile >= '1' and tile <= '9':
        return JellyItem(ord(tile) - ord('1'), left, bottom)
    if tile == 'O' or tile == 'P' or tile == 'Q':
        type = Floor.TYPE_10x2 if tile == 'O' else Floor.TYPE_2x2 if tile == 'P' else Floor.TYPE_3x1
        return Floor(type, left, bottom)
    if tile == 'X':
        return SimpleObstacle(left, bottom)
    if tile == 'Y':
        return AnimObstacle(ANIM_OBSTACLE_INFO[0], left, bottom)
    if tile == 'Z':
        return AnimObstacle(ANIM_OBSTACLE_INFO[1], left, bottom)
    return None

def tile_at(x, y):
    try:
        col = x % UNIT_PER_LINE
        row = x // UNIT_PER_LINE * map_height + map_height - 1 - y
        # print(f'{row=} {col=} {len(lines)=}')
        # print(f'{lines[row]=} {len(lines[row])=}')
        return lines[row][col]
    except:
        return ''

map_height = 10
UNIT_PER_LINE = 100

def init():
    global lines
    with open('res/stage_01.txt') as f:
        lines = f.readlines()

    global map_width, map_height, map_data
    global last_floor_right, map_x
    world = gfw.top().world
    last_floor_right = 0
    map_x = 0
    map_width = len(lines) // map_height * UNIT_PER_LINE
    print(f'{map_width=}')

def draw():
    pass
def update():
    global last_floor_right, map_x

    last_floor_right += SPEED * gfw.frame_time

    while last_floor_right < 17 * UNIT:
        bottom = 0
        for y in range(map_height):
            tile = tile_at(map_x, y)
            obj = mapobject_factory_create(tile, last_floor_right, bottom)
            if obj is not None:
                # print(f'@({map_x}, {y}) {obj} ({obj.x},{obj.y}) [{obj.x - obj.width//2} ~ {obj.x + obj.width//2}]')
                world = gfw.top().world
                world.append(obj)
            bottom += UNIT
        map_x += 1
        last_floor_right += UNIT
        # print(f'{map_x=} / {map_width=}')

