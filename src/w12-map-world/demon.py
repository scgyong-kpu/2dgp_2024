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

    def update(self):
        world = gfw.top().world
        player = world.object_at(world.layer.player, 0)
        angle_radian = math.atan2(player.y - self.y, player.x - self.x)
        self.x += self.speed * math.cos(angle_radian) * gfw.frame_time
        self.y += self.speed * math.sin(angle_radian) * gfw.frame_time

    def draw(self):
        bg = gfw.top().world.bg
        index = self.get_anim_index()
        screen_pos = bg.to_screen(self.x, self.y)
        self.image.clip_draw(index * self.width, 0, self.width, self.height, *screen_pos)

    def get_bb(self):
        l = self.x - self.bb_width // 2
        b = self.y - self.bb_height // 2
        r = self.x + self.bb_width // 2
        t = self.y + self.bb_height // 2
        return l, b, r, t

