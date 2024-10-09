from pico2d import * 
from gfw import *

world = World(['bg'])

canvas_width = 1024
canvas_height = 768
shows_bounding_box = True
shows_object_count = True

def enter():
    world.append(Sprite('res/kpu_1280x960.png', canvas_width // 2, canvas_height // 2), world.layer.bg)
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


if __name__ == '__main__':
    gfw.start_main_module()

