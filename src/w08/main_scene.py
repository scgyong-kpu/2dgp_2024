from pico2d import * 
from gfw import *
from player import Cookie

world = World(['bg', 'player'])

canvas_width = 1280
canvas_height = 720
shows_bounding_box = True
shows_object_count = True

def enter():
    world.append(HorzFillBackground('res/cookie_run_bg_1.png', -10), world.layer.bg)
    world.append(HorzFillBackground('res/cookie_run_bg_2.png', -100), world.layer.bg)
    world.append(HorzFillBackground('res/cookie_run_bg_3.png', -150), world.layer.bg)

    world.append(Sprite('res/cookie.png', 160, 160), world.layer.player)

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

