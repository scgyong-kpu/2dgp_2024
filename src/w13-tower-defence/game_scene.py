from pico2d import * 
from gfw import *
import stage_path
import fly_gen
import collision
import pause_scene
import weapon

tilesize = 48
canvas_width = 32 * tilesize # 1536 = 32 * 48
canvas_height = 18 * tilesize # 864 = 18 * 48
shows_object_count = True
shows_bounding_box = True

world = gfw.World(['bg', 'path', 'weapon', 'bullet', 'fly', 'explosion', 'controller'])


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

    # world.append(BowWeapon(), world.layer.weapon)
    # world.append(IceSword(), world.layer.weapon)
    # world.append(FireThrower(), world.layer.weapon)


def exit():
    world.clear()

def pause():
    print('[main.pause()]')

def resume():
    print('[main.resume()]')

weapon_to_install = None

def handle_event(e):
    global weapon_to_install
    if e.type == SDL_KEYDOWN:
        if e.key == SDLK_ESCAPE:
            gfw.push(pause_scene)
            return True
        if e.key in { SDLK_1, SDLK_2, SDLK_3, SDLK_4 }:
            num = e.key - SDLK_1
            weapon_to_install = weapon.get_weapon(num)
            print(f'{num=} {weapon_to_install=}')
            if weapon_to_install is None: return
            world.append(weapon_to_install)
            return
    elif e.type == SDL_MOUSEMOTION:
        if weapon_to_install is not None:
            x, y = gfw.mouse_xy(e)
            weapon_to_install.x = x
            weapon_to_install.y = y
    elif e.type == SDL_MOUSEBUTTONDOWN:
        if e.button == SDL_BUTTON_LEFT:
            if weapon_to_install is not None:
                weapon_to_install.install()
                weapon_to_install = None

if __name__ == '__main__':
    gfw.start_main_module()

