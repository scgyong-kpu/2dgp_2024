from pico2d import * 
from gfw import *
import stage_path
import random
from functools import reduce
import castle
from cfg import cfg

GEN_INTERVAL_FROM, GEN_INTERVAL_TO = 3.0, 1.0

class Fly(AnimSprite):
    def __init__(self, info):
        # x = random.randint(100, get_canvas_width() - 100)
        # y = random.randint(100, get_canvas_height() - 100)
        x, y = stage_path.spawn_pos() # spawn position
        x += random.uniform(-10, 10)
        y += random.uniform(-10, 10)
        super().__init__(info.file, x, y, info.fps)
        self.layer_index = world.layer.fly
        self.info = info
        self.speed = random.uniform(*info.speed)
        self.path_index = 1
        self.max_life = info.life
        self.life = self.max_life
        self.gauge = Gauge('res/gauge_fg.png', 'res/gauge_bg.png')
        self.angle = 0
        self.stun_timer = 0
        self.hit_timer = 0
        self.set_target_position()

    def set_target_position(self):
        if self.path_index >= len(stage_path.path_coords):
            self.dx, self.dy = 0, 0
            return False
        self.tx, self.ty = stage_path.path_coords[self.path_index]
        self.tx += random.uniform(-10, 10)
        self.ty += random.uniform(-10, 10)
        # print(f'{(self.tx, self.ty)=}')
        dx, dy = self.tx - self.x, self.ty - self.y
        dist = math.sqrt(dx ** 2 + dy ** 2)
        self.dx, self.dy = dx / dist, dy / dist
        self.angle = math.atan2(dy, dx)
        # print(f'{(self.dx, self.dy)=}')
        return True

    def draw(self):
        index = self.get_anim_index()
        self.image.clip_composite_draw(index * self.width, 0, self.width, self.height, self.angle, '', self.x, self.y, self.width, self.height)
        gx, gy = self.x, self.y - 24
        self.gauge.draw(gx, gy, self.width - 28, self.life / self.max_life)

    def hit(self, damage): #return True if dead
        self.life -= damage
        dead = self.life <= 0
        if dead:
            gold = gfw.top().gold
            gold.score += self.max_life // 10
        return dead

    def get_bb(self):
        l,b,r,t = self.info.bbox
        return self.x+l, self.y+b, self.x+r, self.y+t

    def make_stunned(self, seconds):
        self.stun_timer = seconds

    def update(self):
        if self.stun_timer > 0:
            self.stun_timer -= gfw.frame_time
            return
        self.x += self.dx * self.speed * gfw.frame_time
        self.y += self.dy * self.speed * gfw.frame_time
        dx, dy = self.tx - self.x, self.ty - self.y
        if dx < -1 or 1 < dx or dy < -1 or 1 < dy:
            # print(f'{(dx, dy)=}')
            return
        dist = math.sqrt(dx ** 2 + dy ** 2)
        # print(dist)
        if dist < 1:
            self.path_index += 1
            moving = self.set_target_position()
            if not moving:
                self.hit_castle()
        # print(f'({self.dx:.1f}, {self.dy:.1f}) ({self.x=:.1f}, {self.y=:.1f}) {self.speed=} * {gfw.frame_time=:.2f} {self.dx * self.speed * gfw.frame_time}')
    def hit_castle(self):
        if self.hit_timer > 0:
            self.hit_timer -= gfw.frame_time
            return
        castle.hit(self.info.power)
        self.hit_timer = self.info.cool_time

# module itself as Fly Generator

def init():
    global world
    world = gfw.top().world
    global time
    time = 0

    global type
    type = 1

    global interval
    interval = GEN_INTERVAL_FROM

def draw(): pass
def update():
    global time, type, interval
    time -= gfw.frame_time
    if time <= 0:
        interval -= 1/30
        if interval >= GEN_INTERVAL_TO:
            time = interval
            generate()

def cleared():
    return interval < GEN_INTERVAL_TO and world.count_at(world.layer.fly) == 0

rate_sum = reduce(lambda sum, i: sum + i.rate, cfg.flies, 0)
# print(f'{rate_sum=}')

def generate():
    val = random.randrange(rate_sum)
    for info in cfg.flies:
        val -= info.rate
        if val < 0: break
    else:
        return
    world.append(Fly(info))



