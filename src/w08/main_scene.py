from pico2d import * 
from gfw import *
from player import Cookie
import floor

world = World(['bg', 'floor', 'item', 'obstacle', 'player', 'controller'])

canvas_width = 1152 #1280
canvas_height = 648 #720
shows_bounding_box = True
shows_object_count = True

def enter():
    world.append(HorzFillBackground('res/cookie_run_bg_1.png', -10), world.layer.bg)
    world.append(HorzFillBackground('res/cookie_run_bg_2.png', -100), world.layer.bg)
    world.append(HorzFillBackground('res/cookie_run_bg_3.png', -150), world.layer.bg)

    floor.init()
    world.append(floor, world.layer.controller)

    global cookie
    cookie_info = {
      "id": "107572",
      "name": "Coffee Cookie",
      "type": "13x6",
      "size": 320
    }
    cookie = Cookie(cookie_info)
    world.append(cookie, world.layer.player)

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

    cookie.handle_event(e)

if __name__ == '__main__':
    gfw.start_main_module()

