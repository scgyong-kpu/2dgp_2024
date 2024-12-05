from pico2d import * 
from gfw import *
import stage_path
import fly_gen
import collision
import pause_scene
from weapon import *

tilesize = 48
canvas_width = 32 * tilesize # 1536 = 32 * 48
canvas_height = 18 * tilesize # 864 = 18 * 48
shows_object_count = True
shows_bounding_box = True

world = gfw.World(['bg', 'path', 'weapon', 'bullet', 'fly', 'controller'])


stage = 1
# stage = 2
# stage = 3


def enter():
    global bg
    bg = MapBackground(f'res/map/stage_{stage:02d}.json', tilesize=tilesize, wraps=False)
    world.append(bg, world.layer.bg)

    stage_path.set_tile_bg(bg)
    # map_path = stage_path.path_shower()
    # world.append(map_path, world.layer.path)

    fly_gen.init()
    world.append(fly_gen, world.layer.controller)

    
    world.append(collision, world.layer.controller)

    world.append(BowWeapon(), world.layer.weapon)

    world.append(AnimSprite('res/bullet_snow.png', 500, 500, 10), world.layer.bullet)


def exit():
    world.clear()

def pause():  
    print('[main.pause()]')

def resume():
    print('[main.resume()]')

def handle_event(e):
    if e.type == SDL_KEYDOWN and e.key == SDLK_1:
        print(world.objects)
        print(bg.tmap)
        return
    if e.type == SDL_KEYDOWN and e.key == SDLK_ESCAPE:
        gfw.push(pause_scene)
        return True

if __name__ == '__main__':
    gfw.start_main_module()

