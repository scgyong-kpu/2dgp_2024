from pico2d import * 
# SDL_*, SDLK_* 상수를 쓰려면 선언해야 한다

import gfw
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
    if e.type == SDL_KEYDOWN and e.key == SDLK_RETURN:
        gfw.push(sub_scene)
        return True # 이 이벤트는 처리했음을 알린다

    boy.handle_event(e)

if __name__ == '__main__':
    gfw.start_main_module()

