import math
from pico2d import * 
from gfw import *

class Demon(AnimSprite):
    def __init__(self, x, y):
        super().__init__('res/demon_itsumade.png', x, y, 10)
        self.layer_index = gfw.top().world.layer.enemy
        self.speed = 100
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

