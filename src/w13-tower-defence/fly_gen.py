from pico2d import * 
from gfw import *
import stage_path
import random
from functools import reduce

class Info:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

FLY_TYPES = [
    Info(file='res/fly_1.png', fps=3, speed=(5,10), rate=5,  bbox=(-20,-20,20,20), life=900),
    Info(file='res/fly_2.png', fps=3, speed=(10,30), rate=10, bbox=(-20,-20,20,20), life=300),
    Info(file='res/fly_3.png', fps=3, speed=(20,30), rate=15, bbox=(-20,-20,20,20), life=200),
    Info(file='res/fly_4.png', fps=2, speed=(30,40), rate=25, bbox=(-20,-20,20,20), life=150),
    Info(file='res/fly_5.png', fps=1, speed=(30,40), rate=35, bbox=(-20,-20,20,20), life=80),
]

GEN_INTERVAL = 1.0
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
        self.set_target_position()

    def set_target_position(self):
        if self.path_index >= len(stage_path.path_coords):
            self.dx, self.dy = 0, 0
            return
        self.tx, self.ty = stage_path.path_coords[self.path_index]
        self.tx += random.uniform(-10, 10)
        self.ty += random.uniform(-10, 10)
        # print(f'{(self.tx, self.ty)=}')
        dx, dy = self.tx - self.x, self.ty - self.y
        dist = math.sqrt(dx ** 2 + dy ** 2)
        self.dx, self.dy = dx / dist, dy / dist
        self.angle = math.atan2(dy, dx)
        # print(f'{(self.dx, self.dy)=}')

    def get_bb(self):
        l,b,r,t = self.info.bbox
        return self.x+l, self.y+b, self.x+r, self.y+t

    def draw(self):
        index = self.get_anim_index()
        self.image.clip_composite_draw(index * self.width, 0, self.width, self.height, self.angle, '', self.x, self.y, self.width, self.height)
        gx, gy = self.x, self.y - 24
        self.gauge.draw(gx, gy, self.width - 28, self.life / self.max_life)

    def hit(self, damage): #return True if dead
        self.life -= damage
        return self.life <= 0

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
            self.set_target_position()
        # print(f'({self.dx:.1f}, {self.dy:.1f}) ({self.x=:.1f}, {self.y=:.1f}) {self.speed=} * {gfw.frame_time=:.2f} {self.dx * self.speed * gfw.frame_time}')


# module itself as Fly Generator

def init():
    global world
    world = gfw.top().world
    global time
    time = 0

    global type
    type = 1


def draw(): pass
def update():
    global time, type
    time -= gfw.frame_time
    if time <= 0:
        time += GEN_INTERVAL
        generate()

rate_sum = reduce(lambda sum, i: sum + i.rate, FLY_TYPES, 0)
# print(f'{rate_sum=}')

def generate():
    val = random.randrange(rate_sum)
    for info in FLY_TYPES:
        val -= info.rate
        if val < 0: break
    else:
        return
    world.append(Fly(info))


