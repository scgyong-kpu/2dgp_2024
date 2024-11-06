from pico2d import * 
from gfw import *

world = World(2)

import sys
self = sys.modules[__name__]

def enter():
    global frame_9p
    frame_9p = gfw.image.NinePatch(gfw.image.load('res/hs_frame.png'), 30, 30, 30, 30)
    global font
    font = gfw.font.load('res/ENCR10B.TTF', 30)
    world.append(self, 1)

def exit():
    world.clear()

def update():
    pass

def draw():
    cw, ch = get_canvas_width(), get_canvas_height()
    frame_9p.draw(cw // 2, ch // 2, cw - 100, ch - 100)

def pause():
    print('[main.pause()]')

def resume():
    print('[main.resume()]')

def handle_event(e):
    if e.type == SDL_KEYDOWN and e.key == SDLK_1:
        print(world.objects)
        return

if __name__ == '__main__':
    gfw.start_main_module()

