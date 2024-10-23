from pico2d import * 
from gfw import *

world = World()

canvas_width = 1280
canvas_height = 720
shows_bounding_box = True
shows_object_count = True

def enter():
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

