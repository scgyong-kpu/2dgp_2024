from pico2d import * 
from gfw import *

class Demon(AnimSprite):
    def __init__(self, x, y):
        super().__init__('res/demon_itsumade.png', x, y, 10)
        self.layer_index = gfw.top().world.layer.enemy
        self.bb_width = 30
        self.bb_height = 30

    def get_bb(self):
        l = self.x - self.bb_width // 2
        b = self.y - self.bb_height // 2
        r = self.x + self.bb_width // 2
        t = self.y + self.bb_height // 2
        return l, b, r, t

