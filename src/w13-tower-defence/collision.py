from pico2d import * 
from gfw import *

def draw(): pass

def update():
    world = gfw.top().world
    for e in world.objects_at(world.layer.fly):
        for b in world.objects_at(world.layer.bullet):
            if collides_box(e, b):
                if e.hit(b.power):
                    world.remove(e)
                world.remove(b)
                break