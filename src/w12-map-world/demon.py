import math
import random
from pico2d import * 
from gfw import *

INFO = [
    ('res/demon_itsumade.png', 0, 50, 100, -15, -15, 15, 15),
    ('res/demon_mizar.png', 12, 20, 50, -28, -5, 8, 31),
    ('res/demon_lion.png', 8, 40, 60, -25, -14, 25, 14),
]

class Demon(AnimSprite):
    def __init__(self, type, x, y):
        fn, cnt, sp1, sp2 = INFO[type][:4]
        super().__init__(fn, x, y, random.uniform(9, 11), cnt)
        self.layer_index = gfw.top().world.layer.enemy
        self.speed = random.uniform(sp1, sp2)
        self.info = INFO[type]
        self.flip = ''

    def update(self):
        world = gfw.top().world
        player = world.object_at(world.layer.player, 0)
        diff_x, diff_y = player.x - self.x, player.y - self.y
        dist = math.sqrt(diff_x ** 2 + diff_y ** 2)
        if dist >= 1:
            dx = self.speed * diff_x / dist * gfw.frame_time
            self.x += dx
            self.y += self.speed * diff_y / dist * gfw.frame_time
            self.flip = 'h' if dx > 0 else ''

    def draw(self):
        bg = gfw.top().world.bg
        index = self.get_anim_index()
        screen_pos = bg.to_screen(self.x, self.y)
        self.image.clip_composite_draw(index * self.width, 0, self.width, self.height, 0, self.flip, *screen_pos, self.width, self.height)

    def get_bb(self):
        l, b, r, t = self.info[4:8]
        if self.flip == 'h':
            l,r = -r,-l
        return self.x+l, self.y+b, self.x+r, self.y+t

def position_somewhere_outside_screen():
    # MARGIN = -100
    MARGIN = 50
    bg = gfw.top().world.bg
    cw, ch = get_canvas_width(), get_canvas_height()
    l, b = bg.from_screen(0, 0)
    r, t = bg.from_screen(cw, ch)
    side = random.randint(1, 4)
    if side == 1: # left
        x, y = l - MARGIN, b + random.random() * ch
    elif side == 2: # bottom
        x, y = l + random.random() * cw, b - MARGIN
    elif side == 3: # right
        x, y = r + MARGIN, b + random.random() * ch
    else: # side == 4, up
        x, y = l + random.random() * cw, t + MARGIN
    # print(f'{side=} {(x,y)=}')
    return x, y

class DemonGen:
    def draw(self): pass
    def update(self):
        world = gfw.top().world
        if world.count_at(world.layer.enemy) >= 10: return
        type = random.randrange(len(INFO))
        x, y = position_somewhere_outside_screen()
        demon = Demon(type, x, y)
        world.append(demon)