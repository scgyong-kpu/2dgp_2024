from pico2d import * 
from gfw import *

world = World(['bg', 'block', 'ui'])

canvas_width = 520
canvas_height = 600
shows_bounding_box = True
shows_object_count = True

def enter():
    world.append(Background('res/FF9F49.png'), world.layer.bg)
    pass

def exit():
    world.clear()

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

