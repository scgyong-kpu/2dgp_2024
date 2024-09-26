from pico2d import * 
# SDL_*, SDLK_* 상수를 쓰려면 선언해야 한다

import gfw
from grass import Grass
from boy import Boy

import sub_scene

world = gfw.World(3)

def enter():
    global boy
    boy = Boy()
    world.append(boy, 1)
    world.append(Grass(), 0)
''' 레이어 번호를 잘 맞춰주지 않으면 당연히 여러 에러가 발생한다.
Traceback (most recent call last):
  ...(생략)...
  File "D:/Lectures/2024_2/2dgp/git/src/w04/boy.py", line 21, in update
    if not go.bounced: continue
AttributeError: 'Boy' object has no attribute 'bounced'
'''

def exit():
    world.clear()
    print('[main.exit()]')

def pause():
    print('[main.pause()]')

def resume():
    print('[main.resume()]')

def handle_event(e):
    if e.type == SDL_KEYDOWN and e.key == SDLK_RETURN:
        gfw.push(sub_scene)
        return True # 이 이벤트는 처리했음을 알린다
    if e.type == SDL_KEYDOWN and e.key == SDLK_1:
        print(world.objects)

    boy.handle_event(e)

if __name__ == '__main__':
    gfw.start_main_module()

