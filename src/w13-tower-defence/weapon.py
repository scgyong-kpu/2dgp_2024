from pico2d import * 
from gfw import *
import random


class BowWeapon(Sprite):
    def __init__(self):
        x, y = 500, 300
        super().__init__('res/weapon/bow_1.png', x, y)
        self.time = 0
        self.interval = 1.0
        self.angle = 0
    def update(self):
        self.time += gfw.frame_time
        if self.time >= self.interval:
            self.time -= self.interval
            self.fire()
    def draw(self):
        self.image.composite_draw(self.angle, '', self.x, self.y)

    def fire(self):
        pass
