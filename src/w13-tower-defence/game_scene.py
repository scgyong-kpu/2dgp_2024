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

def handle_event(e):
    global weapon_to_install, selected_weapon
    if e.type == SDL_KEYDOWN:
        if e.key == SDLK_ESCAPE:
            gfw.push(pause_scene)
            return True
        if e.key in { SDLK_1, SDLK_2, SDLK_3, SDLK_4 }:
            num = e.key - SDLK_1
            weapon.get_candidate_ready(num)
            return True
        if e.key == SDLK_u:
            weapon.upgrade()
            return True
        if e.key == SDLK_BACKSPACE:
            weapon.uninstall()
    elif e.type == SDL_MOUSEMOTION:
        weapon.move_candidate(*gfw.mouse_xy(e))
        return True
    elif e.type == SDL_MOUSEBUTTONDOWN:
        if e.button == SDL_BUTTON_LEFT:
            weapon.on_click(*gfw.mouse_xy(e))
            return True

if __name__ == '__main__':
    gfw.start_main_module()

