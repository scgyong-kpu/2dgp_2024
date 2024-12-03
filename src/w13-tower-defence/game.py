from pico2d import * 
from gfw import *

canvas_width = 1536 # 32 * 48
canvas_height = 864 # 18 * 48
shows_object_count = True

world = gfw.World(['bg', 'path'])


stage = 1

def enter():
    global bg
    bg = MapBackground(f'res/map/stage_{stage:02d}.json', fitsHeight=True, wraps=False)
    object_layer = bg.tmap.layers[1]

    obj_start, obj_end = object_layer.objects[0:2]
    print(obj_start, obj_end)

def exit():
    world.clear()

# def pause():
#     print('[main.pause()]')

# def resume():
#     print('[main.resume()]')

def handle_event(e):
    if e.type == SDL_KEYDOWN and e.key == SDLK_1:
        print(world.objects)
        print(bg.tmap)
        return

if __name__ == '__main__':
    gfw.start_main_module()

