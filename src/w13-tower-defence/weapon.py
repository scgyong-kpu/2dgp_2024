from pico2d import * 
from gfw import *
import stage_path
import random
from cfg import cfg

class Bullet(AnimSprite):
    SPLASH_DISTANCE_SQUARE = 100 ** 2
    def __init__(self, file, weapon, speed, radius):
        super().__init__(file, weapon.x, weapon.y, 10)
        self.angle = weapon.angle
        self.speed = speed
        self.power = weapon.power
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
    def __init__(self, weapon, speed):
        super().__init__('res/weapon/arrow.png', weapon, speed=speed, radius=15)

class SnowBall(Bullet):
    def __init__(self, weapon, speed):
        super().__init__('res/weapon/bullet_snow.png', weapon, speed=speed, radius=10)
        self.splash = True
        self.stuns = True
    def explosion(self, enemy):
        return Explosion('res/weapon/bullet_snow_explosion.png', *self.pos_between(enemy), 9, 1)

class FireBall(Bullet):
    def __init__(self, weapon, speed):
        super().__init__('res/weapon/fireball.png', weapon, speed=speed, radius=14)
        self.splash = True
    def explosion(self, enemy):
        x, y = self.pos_between(enemy)
        return Explosion('res/weapon/fireball_explosion.png', x, y + 20, 15, 1)

class Weapon(Sprite):
    selected = None
    installing = None
    def __init__(self, bullet_class, cfg):
        file = cfg.fmt % 1
        super().__init__(file, 0, 0)
        self.range_image = gfw.image.load('res/weapon/range.png')
        self.enabled = False
        self.time = 0
        self.angle = 0
        self.bullet_class = bullet_class
        self.layer_index = gfw.top().world.layer.weapon
        self.selected = False
        self.level = 1
        self.cfg = cfg
        self.interval = cfg.interval
        # self.costs = cfg.costs
        self.range = cfg.range
        self.power = cfg.power

    def move_to(self, x, y):
        main_scene = gfw.top()
        tsize = main_scene.bg.tilesize
        x = (int(x / tsize) + 0.5) * tsize
        y = (int(y / tsize) + 0.5) * tsize
        if stage_path.can_install_at(x, y):
            self.x, self.y = x, y
    def select(self, selected):
        self.selected = selected
    def install(self):
        if not stage_path.can_install_at(self.x, self.y):
            return False
        if not self.widthdraw_cost():
            return False
        stage_path.install_at(self.x, self.y, self.cfg.block * self.width)
        self.enabled = True
        return True
    def widthdraw_cost(self):
        gold = gfw.top().gold
        cost = self.cfg.costs[self.level - 1]
        if gold.score < cost:
            return False
        gold.score -= cost
        return True
    def uninstall(self):
        world = gfw.top().world
        world.remove(self)
    def upgrade(self):
        try:
            level = self.level + 1
            file = self.cfg.fmt % level
            image = gfw.image.load(file)
        except:
            print(f'File not found: {file}')
            return

        if not self.widthdraw_cost():
            return

        self.image = image
        self.level = level
        self.range *= cfg.weapon.range_increase
        self.interval *= cfg.weapon.interval_decrease
        self.power *= cfg.weapon.power_increase
    def update(self):
        if not self.enabled: return
        self.time += gfw.frame_time
        found = self.find_neareast_enemy()
        if found and self.time >= self.interval:
            self.time = 0
            self.fire()
    def draw(self):
        if self.selected:
            size = 2 * self.range
            self.range_image.draw(self.x, self.y, size, size)
        self.image.composite_draw(self.angle, '', self.x, self.y)

    def fire(self):
        arrow = self.bullet_class(self, self.cfg.bullet_speed)
        world = gfw.top().world
        world.append(arrow)

    def find_neareast_enemy(self):
        max_dsq = self.range ** 2
        world = gfw.top().world
        min_dsq, enemy = float('inf'), None
        for fly in world.objects_at(world.layer.fly):
            dsq = (fly.x - self.x) ** 2 + (fly.y - self.y) ** 2
            if min_dsq > dsq and dsq <= max_dsq:
                min_dsq, enemy = dsq, fly
                # print(f'{dsq=:-10.2f} {fly=}')

        if enemy is not None:
            self.angle = math.atan2(enemy.y - self.y, enemy.x - self.x)
            return True

        return False

class BowWeapon(Weapon):
    def __init__(self):
        super().__init__(Arrow, cfg.weapon.arrow)

class IceSword(Weapon):
    def __init__(self):
        super().__init__(SnowBall, cfg.weapon.ice)

class FireThrower(Weapon):
    def __init__(self):
        super().__init__(FireBall, cfg.weapon.fire)

WEAPONS = [
    BowWeapon, IceSword, FireThrower
]


def get_candidate_ready(type):
    world = gfw.top().world
    if Weapon.selected is not None:
        Weapon.selected.select(False)
        Weapon.selected = None
    if Weapon.installing is not None:
        pos = Weapon.installing.x, Weapon.installing.y
        world.remove(Weapon.installing, world.layer.weapon)
        world.clear_at(world.layer.path)
    else:
        pos = stage_path.any_install_position()

    try:
        clazz = WEAPONS[type]
        Weapon.installing = clazz()
    except Exception as e:
        Weapon.installing = None
        return

    Weapon.installing.x, Weapon.installing.y = pos
    world.append(Weapon.installing)
    world.append(stage_path.path_shower(), world.layer.path)
    Weapon.selected = Weapon.installing
    Weapon.selected.select(True)

def move_candidate(x, y):
    if Weapon.installing is not None:
        Weapon.installing.move_to(x, y)

def install_candidate():
    installed = False
    if Weapon.installing is not None:
        installed = Weapon.installing.install()
        if installed:
            Weapon.installing = None
            world = gfw.top().world
            world.clear_at(world.layer.path)
    return installed

def select_weapon(x, y):
    if Weapon.selected is not None:
        Weapon.selected.select(False)
    world = gfw.top().world
    for w in world.objects_at(world.layer.weapon):
        if w.contains_xy(x, y):
            Weapon.selected = w
            Weapon.selected.select(True)
            break

def on_click(x, y):
    if install_candidate():
        return
    select_weapon(x, y)

def upgrade():
    if Weapon.selected is not None:
        Weapon.selected.upgrade()

def uninstall():
    if Weapon.selected is not None:
        Weapon.selected.uninstall()
        Weapon.selected = None



