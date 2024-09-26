from pico2d import * 
# SDL_*, SDLK_* 상수를 쓰려면 선언해야 한다

import gfw_loop
from grass import Grass
from boy import Boy

import sub_scene

def enter():
    global boy
    boy = Boy()
    gfw_loop.game_objects.append(boy)
    gfw_loop.game_objects.append(Grass())

def exit():
    gfw_loop.game_objects.clear()

def handle_event(e):
    if e.type == SDL_KEYDOWN:
        if e.key == SDLK_LEFT:
            boy.x -= 10
        elif e.key == SDLK_RIGHT:
            boy.x += 10
        elif e.key == SDLK_RETURN:
            gfw_loop.change(sub_scene)

if __name__ == '__main__':
    gfw_loop.start_main_module()

