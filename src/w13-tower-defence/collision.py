from pico2d import * 
from gfw import *

def draw(): pass

def update():
    world = gfw.top().world
    for b in world.objects_at(world.layer.bullet):
        for e in world.objects_at(world.layer.fly):
            if collides_box(e, b):
                if e.hit(b.power):
                    world.remove(e)
                world.remove(b)
                break