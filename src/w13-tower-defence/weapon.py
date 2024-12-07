from pico2d import * 
from gfw import *
import stage_path
import random


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
        self.splash = False
        self.stuns = False
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

    def explosion(self, enemy):
        return None

    def check_collision(self):
        world = gfw.top().world
        enemy = None
        for e in world.objects_at(world.layer.fly):
            if collides_box(e, self):
                if e.hit(self.power):
                    world.remove(e)
                elif self.stuns: 
                    e.make_stunned(1)
                    enemy = e
                world.remove(self)
                enemy = e
                break
        
        if enemy is None or not self.splash: return

        exp = self.explosion(enemy)
        if exp: world.append(exp)

        for e in world.objects_at(world.layer.fly):
            if e == enemy: continue
            dist_sq = (enemy.x - e.x) ** 2 + (enemy.y - e.y) ** 2
            if dist_sq < self.SPLASH_DISTANCE_SQUARE: 
                power = self.power * (1 - dist_sq / self.SPLASH_DISTANCE_SQUARE)
                # print(f'{dist_sq=:.2f} distance={math.sqrt(dist_sq):.2f} {power=:.2f} {e=}')
                if e.hit(power):
                    world.remove(e)
                elif self.stuns:
                    duration = max(0.5, power / self.power)
                    e.make_stunned(duration)
    def pos_between(self, other):
        return (self.x + other.x) / 2, (self.y + other.y) / 2

class Explosion(AnimSprite):
    def __init__(self, file, x, y, fps, duration):
        super().__init__(file, x, y, fps)
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
        super().__init__('res/weapon/arrow.png', weapon, speed=300, power=50, radius=15)

class SnowBall(Bullet):
    def __init__(self, weapon):
        super().__init__('res/weapon/bullet_snow.png', weapon, speed=200, power=60, radius=10)
        self.splash = True
        self.stuns = True
    def explosion(self, enemy):
        return Explosion('res/weapon/bullet_snow_explosion.png', *self.pos_between(enemy), 9, 1)

class FireBall(Bullet):
    def __init__(self, weapon):
        super().__init__('res/weapon/fireball.png', weapon, speed=160, power=80, radius=14)
        self.splash = True
    def explosion(self, enemy):
        x, y = self.pos_between(enemy)
        return Explosion('res/weapon/fireball_explosion.png', x, y + 20, 15, 1)

class Weapon(Sprite):
    def __init__(self, file, intitial_interval, bullet_class):
        x, y = stage_path.any_install_position()
        super().__init__(file, x, y)
        self.range_image = gfw.image.load('res/weapon/range.png')
        self.enabled = False
        self.time = 0
        self.angle = 0
        self.interval = intitial_interval
        self.bullet_class = bullet_class
        self.layer_index = gfw.top().world.layer.weapon
    def move_to(self, x, y):
        main_scene = gfw.top()
        tsize = main_scene.bg.tilesize
        x = (int(x / tsize) + 0.5) * tsize
        y = (int(y / tsize) + 0.5) * tsize
        if stage_path.can_install_at(x, y):
            self.x, self.y = x, y
    def install(self):
        if stage_path.can_install_at(self.x, self.y):
            stage_path.install_at(self.x, self.y, self.width)
            self.enabled = True
            return True
        return False
    def update(self):
        if not self.enabled: return
        self.find_neareast_enemy()
        self.time += gfw.frame_time
        if self.time >= self.interval:
            self.time -= self.interval
            self.fire()
    def draw(self):
        self.range_image.draw(self.x, self.y, 200, 200)
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
        super().__init__('res/weapon/bow_1.png', 2.0, Arrow)

class IceSword(Weapon):
    def __init__(self):
        super().__init__('res/weapon/ice_sword_1.png', 3.0, SnowBall)

class FireThrower(Weapon):
    def __init__(self):
        super().__init__('res/weapon/fire_thrower.png', 6.0, FireBall)

WEAPONS = [
    BowWeapon, IceSword, FireThrower
]

def get_weapon(type):
    try:
        clazz = WEAPONS[type]
        return clazz()
    except Exception as e:
        print(e)
        return None

