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
    layer = bg.tmap.layers[1]

    o1, o2 = layer.objects[0:2]
    start_pos = o1['x'], o1['y']
    end_pos = o2['x'], o2['y']

    print(f'{start_pos=}, {end_pos=:}')

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

