from pico2d import * 
from gfw import *
import random


class Arrow(Sprite):
    def __init__(self, bow):
        super().__init__('res/arrow.png', bow.x, bow.y)
        self.angle = bow.angle
        self.speed = 100
        self.dx = self.speed * math.cos(self.angle)
        self.dy = self.speed * math.sin(self.angle)
    def update(self):
        self.x += self.dx * gfw.frame_time
        self.y += self.dy * gfw.frame_time

        if self.x < 0 or self.x > get_canvas_width() or \
            self.y < 0 or self.y > get_canvas_height():
            world = gfw.top().world
            world.remove(self, world.layer.bullet)

    def draw(self):
        self.image.composite_draw(self.angle, '', self.x, self.y)

class BowWeapon(Sprite):
    def __init__(self):
        x, y = 500, 300
        super().__init__('res/bow_1.png', x, y)
        self.time = 0
        self.interval = 1.0
        self.angle = 1.0 # 57.3 degree
    def update(self):
        self.find_neareast_enemy()
        self.time += gfw.frame_time
        if self.time >= self.interval:
            self.time -= self.interval
            self.fire()
    def draw(self):
        self.image.composite_draw(self.angle, '', self.x, self.y)

    def fire(self):
        arrow = Arrow(self)
        world = gfw.top().world
        world.append(arrow, world.layer.bullet)

    def find_neareast_enemy(self):
        world = gfw.top().world
        min_dsq, enemy = float('inf'), None
        for fly in world.objects_at(world.layer.fly):
            dsq = (fly.x - self.x) ** 2 + (fly.y - self.y) ** 2
            if min_dsq > dsq:
                min_dsq, enemy = dsq, fly
                # print(f'{dsq=:-10.2f} {fly=}')

        if enemy is not None:
            self.angle = math.atan2(enemy.y - self.y, enemy.x - self.x)
            # print(f'{fly=} {self.angle=:.2f}')

