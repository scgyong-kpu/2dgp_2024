from pico2d import * 
from gfw import *

world = World()

canvas_width = 960
canvas_height = 540
shows_bounding_box = True
shows_object_count = True

center_x = canvas_width // 2
center_y = canvas_height // 2

def enter():
    world.append(Background('res/bg_andromeda.png'), 0)
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

