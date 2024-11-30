from pico2d import * 
from gfw import *
import stage_path
import random

GEN_INTERVAL = 1.0
class Fly(AnimSprite):
    def __init__(self, type):
        x, y = stage_path.path_coords[0] # spawn position
        # x = random.randint(100, get_canvas_width() - 100)
        # y = random.randint(100, get_canvas_height() - 100)
        super().__init__(f'res/fly_{type}.png', x, y, 3)
        self.layer_index = world.layer.fly
        self.speed = 100
        self.path_index = 1
        self.set_target_position()
        print(f'{(self.x, self.y)=}')

    def set_target_position(self):
        if self.path_index >= len(stage_path.path_coords):
            self.dx, self.dy = 0, 0
            return
        self.tx, self.ty = stage_path.path_coords[self.path_index]
        print(f'{(self.tx, self.ty)=}')
        dx, dy = self.tx - self.x, self.ty - self.y
        dist = math.sqrt(dx ** 2 + dy ** 2)
        self.dx, self.dy = dx / dist, dy / dist
        # print(f'{(self.dx, self.dy)=}')

    def update(self):
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
        world.append(Fly(type))
        type += 1
        if type > 5: type = 1

