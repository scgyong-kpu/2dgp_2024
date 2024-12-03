from pico2d import * 
from gfw import *
# import stage_path
import random

GEN_INTERVAL = 1.0
class Fly(AnimSprite):
    def __init__(self, type):
        x = random.randint(100, get_canvas_width() - 100)
        y = random.randint(100, get_canvas_height() - 100)
        super().__init__(f'res/fly_{type}.png', x, y, 3)
        self.layer_index = world.layer.fly

    # def update(self):
    #     self.x += 100 * gfw.frame_time


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


