from pico2d import * 
from gfw import *
import stage_path

def init():
    global castle_image, x, y
    castle_image = gfw.image.load('res/castle.png')
    x, y = stage_path.castle_pos()
    y += 48

def draw():
    castle_image.draw(x, y)
    print(x,y)

def update():
    pass

def get_bb():
    return x - 70, y - 70, x + 70, y + 70
