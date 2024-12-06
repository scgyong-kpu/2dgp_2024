from pico2d import * 
from gfw import *

def draw(): pass

def update():
    world = gfw.top().world
    for b in world.objects_at(world.layer.bullet):
        b.check_collision()

