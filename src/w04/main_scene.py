from pico2d import * 
# SDL_*, SDLK_* 상수를 쓰려면 선언해야 한다

import gfw_loop
from grass import Grass
from boy import Boy

def enter():
    global boy
    boy = Boy()
    gfw_loop.game_objects.append(boy)
    gfw_loop.game_objects.append(Grass())

def handle_event(e):
    if e.type == SDL_KEYDOWN:
        if e.key == SDLK_LEFT:
            boy.x -= 10
        elif e.key == SDLK_RIGHT:
            boy.x += 10

import sys
scene = sys.modules['__main__'] 
# 시스템으로부터 __main__ 이라는 이름을 가진 module 객체를 얻어낸다

gfw_loop.start(scene)


