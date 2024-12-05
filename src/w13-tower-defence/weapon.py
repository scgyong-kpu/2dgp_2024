from pico2d import * 
from gfw import *
import random

INITIAL_SNOW_INTERVAL = 3.0
INITIAL_ARROW_INTERVAL = 2.0
INITIAL_FIRE_INTERVAL = 6.0

class Bullet(AnimSprite):
    SPLASH_DISTANCE_SQUARE = 100 ** 2
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
            world.remove(self)

    def draw(self):
        index = self.get_anim_index()
        self.image.clip_composite_draw(index * self.width, 0, self.width, self.height, self.angle, '', self.x, self.y, self.width, self.height)

    def get_bb(self):
        return self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius

    def explosion(self):
        return None

    def check_collision(self):
        self.hittest_enemies()

    def hittest_enemies(self, splash=False, stuns=False):
        world = gfw.top().world
        didHit = False
        enemy = None
        for e in world.objects_at(world.layer.fly):
            if collides_box(e, self):
                if e.hit(self.power):
                    world.remove(e)
                elif stuns: 
                    e.make_stunned(1)
                    enemy = e
                world.remove(self)
                didHit = True
                break
        
        if not didHit or not splash: return

        exp = self.explosion()
        if exp: world.append(exp)

        for e in world.objects_at(world.layer.fly):
            if e == enemy: continue
            dist_sq = (self.x - e.x) ** 2 + (self.y - e.y) ** 2
            if dist_sq < self.SPLASH_DISTANCE_SQUARE: 
                power = self.power * (1 - dist_sq / self.SPLASH_DISTANCE_SQUARE)
                print(f'{dist_sq=:.2f} distance={math.sqrt(dist_sq):.2f} {power=:.2f} {e=}')
                if e.hit(power):
                    world.remove(e)
                elif stuns:
                    duration = max(0.5, power / self.power)
                    e.make_stunned(duration)

class Explosion(AnimSprite):
    def __init__(self, file, bullet, fps, duration):
        super().__init__(file, bullet.x, bullet.y, fps)
        self.duration = duration
        self.layer_index = gfw.top().world.layer.explosion
    def update(self):
        # super().update()
        self.duration -= gfw.frame_time
        if self.duration > 0: return
        world = gfw.top().world
        world.remove(self)



class Arrow(Bullet):
    def __init__(self, weapon):
        super().__init__('res/arrow.png', weapon, speed=300, power=50, radius=15)

class SnowBall(Bullet):
    def __init__(self, weapon):
        super().__init__('res/bullet_snow.png', weapon, speed=200, power=60, radius=10)
    def explosion(self):
        return Explosion('res/bullet_snow_explosion.png', self, 9, 1)

    def check_collision(self):
        self.hittest_enemies(splash=True, stuns=True)

class FireBall(Bullet):
    def __init__(self, weapon):
        super().__init__('res/fireball.png', weapon, speed=160, power=80, radius=14)
    def explosion(self):
        return Explosion('res/fireball_explosion.png', self, 15, 1)

    def check_collision(self):
        self.hittest_enemies(splash=True, stuns=True)


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

    def get_bb(self):
        return self.x - 40, self.y - 40, self.x + 40, self.y + 40

class BowWeapon(Weapon):
    def __init__(self):
        super().__init__('res/bow_1.png', 500, 300, INITIAL_ARROW_INTERVAL, Arrow)

class IceSword(Weapon):
    def __init__(self):
        super().__init__('res/ice_sword_1.png', 400, 600, INITIAL_SNOW_INTERVAL, SnowBall)

class FireThrower(Weapon):
    def __init__(self):
        super().__init__('res/fire_thrower.png', 500, 500, INITIAL_FIRE_INTERVAL, FireBall)


