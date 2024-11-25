import math
import random
from pico2d import * 
from gfw import *

class Demon(AnimSprite):
    def __init__(self, x, y, speed=100):
        super().__init__('res/demon_itsumade.png', x, y, random.uniform(9, 11))
        self.layer_index = gfw.top().world.layer.enemy
        self.speed = speed
        self.bb_width = 30
        self.bb_height = 30
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
        l = self.x - self.bb_width // 2
        b = self.y - self.bb_height // 2
        r = self.x + self.bb_width // 2
        t = self.y + self.bb_height // 2
        return l, b, r, t

def position_somewhere_outside_screen():
    # MARGIN = -100
    MARGIN = 100
    bg = gfw.top().world.bg
    cw, ch = get_canvas_width(), get_canvas_height()
    l, b = bg.from_screen(0, 0)
    r, t = bg.from_screen(cw, ch)
    side = random.randint(1, 4)
    if side == 1: # left
        x, y = l - MARGIN, random.random() * ch
    elif side == 2: # bottom
        x, y = random.random() * cw, b - MARGIN
    elif side == 3: # right
        x, y = cw + MARGIN, random.random() * ch
    else: # side == 4, up
        x, y = random.random() * cw, ch + MARGIN
    return x, y

class DemonGen:
    def draw(self): pass
    def update(self):
        world = gfw.top().world
        if world.count_at(world.layer.enemy) >= 10: return
        speed = random.uniform(50, 100)
        x, y = position_somewhere_outside_screen()
        demon = Demon(x, y, speed=speed)
        world.append(demon)