from pico2d import * 
from gfw import *
from player import Cookie
import floor
import pause_scene

world = World(['bg', 'floor', 'item', 'obstacle', 'player', 'controller'])

canvas_width = 1152 #1280
canvas_height = 648 #720
shows_bounding_box = True
shows_object_count = True

cookie_info = {
    "id": "107572",
    "name": "Coffee Cookie",
    "type": "13x6",
    "size": 320
}

def enter():
    world.append(HorzFillBackground('res/cookie_run_bg_1.png', -10), world.layer.bg)
    world.append(HorzFillBackground('res/cookie_run_bg_2.png', -100), world.layer.bg)
    world.append(HorzFillBackground('res/cookie_run_bg_3.png', -150), world.layer.bg)

    floor.init()
    world.append(floor, world.layer.controller)

    global cookie
    cookie = Cookie(cookie_info)
    world.append(cookie, world.layer.player)

    global music
    music = gfw.sound.music('res/sounds/main.mp3')
    music.repeat_play()

def exit():
    music.stop()
    world.clear()

def pause():
    print('[main.pause()]')
    music.pause()

def resume():
    print('[main.resume()]')
    music.resume()

def handle_event(e):
    if e.type == SDL_KEYDOWN and e.key == SDLK_1:
        print(world.objects)
        return

    if e.type == SDL_KEYDOWN and e.key == SDLK_ESCAPE:
        gfw.push(pause_scene)
        return True

    cookie.handle_event(e)

if __name__ == '__main__':
    gfw.start_main_module()

