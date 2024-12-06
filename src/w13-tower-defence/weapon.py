from pico2d import * 
from gfw import *
import random


class Bullet(AnimSprite):
    def __init__(self, file, weapon, speed, power, radius):
        super().__init__(file, weapon.x, weapon.y, 10)
        self.angle = weapon.angle
        self.speed = speed
        self.power = power
        self.radius = radius
        self.dx = speed * math.cos(self.angle)
        self.dy = speed * math.sin(self.angle)
        self.layer_index = gfw.top().world.layer.bullet

    def update(self):
        self.x += self.dx * gfw.frame_time
        self.y += self.dy * gfw.frame_time

        if self.x < 0 or self.x > get_canvas_width() or \
            self.y < 0 or self.y > get_canvas_height():
            world = gfw.top().world
            world.remove(self, world.layer.bullet)

    def draw(self):
        index = self.get_anim_index()
        self.image.clip_composite_draw(index * self.width, 0, self.width, self.height, self.angle, '', self.x, self.y, self.width, self.height)

    def get_bb(self):
        return self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius

class Arrow(Bullet):
    def __init__(self, weapon):
        super().__init__('res/weapon/arrow.png', weapon, speed=300, power=50, radius=15)

class SnowBall(Bullet):
    def __init__(self, weapon):
        super().__init__('res/weapon/bullet_snow.png', weapon, speed=200, power=60, radius=10)

class Weapon(Sprite):
    def __init__(self, file, x, y, intitial_interval, bullet_class):
        # x, y = 500, 300
        super().__init__(file, x, y)
        self.time = 0
        self.angle = 0
        self.interval = intitial_interval
        self.bullet_class = bullet_class
    def update(self):
        self.find_neareast_enemy()
        self.time += gfw.frame_time
        if self.time >= self.interval:
            self.time -= self.interval
            self.fire()
    def draw(self):
        self.image.composite_draw(self.angle, '', self.x, self.y)

    def fire(self):
        arrow = self.bullet_class(self)
        world = gfw.top().world
        world.append(arrow)

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

class BowWeapon(Weapon):
    def __init__(self):
        super().__init__('res/weapon/bow_1.png', 500, 300, 2.0, Arrow)

class IceSword(Weapon):
    def __init__(self):
        super().__init__('res/weapon/ice_sword_1.png', 400, 600, 3.0, SnowBall)
