from pico2d import * 
from gfw import *
import game_scene

canvas_width = game_scene.canvas_width
canvas_height = game_scene.canvas_height
tilesize = game_scene.tilesize

import sys
self = sys.modules[__name__]

world = gfw.World(['bg', 'button'])

def enter():
    world.append(self, world.layer.bg)
    global tile_img
    tile_img = gfw.image.load('res/select_bg_tile.png')
def exit():
    world.clear()
def update(): pass
def draw():
    for y in range(0, canvas_height, tilesize):
        for x in range(0, canvas_width, tilesize):
            tile_img.draw_to_origin(x, y, tilesize, tilesize)
def pause():
    print('[select.pause()]')
def resume():
    print('[select.resume()]')
def handle_event(e):
    pass

if __name__ == '__main__':
    gfw.start_main_module()


