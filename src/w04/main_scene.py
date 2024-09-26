from pico2d import * 
# SDL_*, SDLK_* 상수를 쓰려면 선언해야 한다

import gfw_loop
from grass import Grass
from boy import Boy

import sub_scene

game_objects = []

def enter():
    global boy
    boy = Boy()
    game_objects.append(boy)
    game_objects.append(Grass())

def exit():
    game_objects.clear()
    print('[main.exit()]')

def pause():
    print('[main.pause()]')

def resume():
    print('[main.resume()]')

def handle_event(e):
    if e.type == SDL_KEYDOWN:
        if e.key == SDLK_LEFT:
            boy.x -= 10
        elif e.key == SDLK_RIGHT:
            boy.x += 10
        elif e.key == SDLK_RETURN:
            gfw_loop.push(sub_scene)
            # sub_scene 으로 전환하는 것이 아니고 내 위에 쌓는다

if __name__ == '__main__':
    gfw_loop.start_main_module()

