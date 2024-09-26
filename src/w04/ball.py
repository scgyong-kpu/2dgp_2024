from pico2d import *
from random import randrange, uniform
import gfw

class Ball:
    def __init__(self, x=None, y=None):
        self.image = gfw.image.load('ball_41x41.png')
        self.x = randrange(100, 700) if x is None else x
        self.y = randrange(100, 500) if y is None else y
        self.dx = uniform(1.0, 2.0) * (1 if randrange(2) == 0 else -1)
        self.dy = uniform(1.0, 2.0) * (1 if randrange(2) == 0 else -1)
        self.bounced = False
    def draw(self):
        self.image.draw(self.x, self.y)
    def update(self):
        self.x += self.dx
        self.y += self.dy
        l,t,r,b = 25,35,25,35
        if (self.dx < 0 and self.x < l) or (self.dx > 0 and self.x > get_canvas_width() - r):
            self.dx *= -1
            self.bounced = True
        if (self.dy < 0 and self.y < t) or (self.dy > 0 and self.y > get_canvas_height() - b):
            self.dy *= -1
            self.bounced = True
