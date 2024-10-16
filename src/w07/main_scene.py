from pico2d import * 
from gfw import *
from boy import Boy
from zombie import Zombie

world = World(['bg', 'zombie', 'player'])

canvas_width = 1024
canvas_height = 768
# canvas_width = 1280
# canvas_height = 960
shows_bounding_box = True
shows_object_count = True

def enter():
    global bg
    bg = InfiniteScrollBackground('res/kpu_1280x960.png', margin=100)
    world.append(bg, world.layer.bg)
    world.bg = bg

    for i in range(1):
        world.append(Zombie(), world.layer.zombie)

    global boy
    boy = Boy()
    boy.bg = bg
    world.append(boy, world.layer.player)

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

    if e.type == SDL_KEYDOWN and e.key == SDLK_s:
        world.save('zombies.pickle')
        return

    if e.type == SDL_MOUSEBUTTONDOWN:
        world.append(Zombie(), world.layer.zombie)

    boy.handle_event(e)

if __name__ == '__main__':
    gfw.start_main_module()

