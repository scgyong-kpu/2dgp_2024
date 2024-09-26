from pico2d import *
from random import randrange, uniform
import gfw

GRAVITY = 9.8 * 100

class Ball:
    def __init__(self, player):
        self.image = gfw.image.load('ball_41x41.png')
        self.x, self.y = player.x, player.y
        self.dx = uniform(100, 500)
        max_power = 2 * (get_canvas_height() - player.y)
        self.dy = uniform(100, max_power) # initial power
        if player.action % 2 == 0:
          self.dx *= -1
        self.layer_index = gfw.top().world.layer.ball
    def draw(self):
        self.image.draw(self.x, self.y)
    def update(self):
        self.x += self.dx * gfw.frame_time
        self.y += self.dy * gfw.frame_time

        l,r,b = -25, get_canvas_width()+25, 20
        if self.x < l or r < self.x:
            gfw.top().world.remove(self)
            return
        if self.dy < 0 and self.y <= b: # 공이 아래로 떨어지고 있는 것을 확인해야 한다
            self.dy *= -0.8
            self.dx *= 0.8
            if self.dy < 1 or (-1 < self.dx and self.dx < 1):
                gfw.top().world.remove(self)
                return
        else:
            self.dy -= GRAVITY * gfw.frame_time

    def __repr__(self):
        return f'Ball({self.x:.1f},{self.y:.1f})'
