from pico2d import * 
# SDL_*, SDLK_* 상수를 쓰려면 선언해야 한다

import gfw
from grass import Grass
from boy import Boy

import sub_scene

world = gfw.World(['bg', 'player', 'ball'])

def enter():
    global boy
    boy = Boy()
    world.append(boy, world.layer.player)
    world.append(Grass())
''' 한 번만 추가하는 객체는 객체가 layer_index 를 가지고 있는 것이 오히려 불편하다
Traceback (most recent call last):
  ...(생략)...
  File "D:/Lectures/2024_2/2dgp/git/src/w04/main_scene.py", line 16, in enter
    world.append(Grass())
  File "D:/Lectures/2024_2/2dgp/git/src/w04/gfw_world.py", line 18, in append
    layer_index = go.layer_index
AttributeError: 'Grass' object has no attribute 'layer_index'
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

