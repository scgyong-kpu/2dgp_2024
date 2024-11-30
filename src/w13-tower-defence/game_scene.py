from pico2d import * 
from gfw import *
import stage_path
import fly_gen

canvas_width = 1536 # 32 * 48
canvas_height = 864 # 18 * 48
shows_object_count = True

world = gfw.World(['bg', 'path', 'fly', 'controller'])

stage = 1

def enter():
    global bg
    json_fn = f'res/map/stage_{stage:02d}.json'
    bg = MapBackground(json_fn, fitsHeight=True, wraps=False)

    world.append(bg, world.layer.bg)
    world.bg = bg

    stage_path.set_tile_bg(bg)
    # map_path = stage_path.path_shower()
    # world.append(map_path, world.layer.path)

    fly_gen.init()
    world.append(fly_gen, world.layer.controller)


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

