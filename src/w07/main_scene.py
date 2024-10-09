from pico2d import * 
from gfw import *
from boy import Boy

world = World(['bg', 'player'])

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

    # if e.type == SDL_KEYDOWN:
    #     if e.key == SDLK_LEFT:
    #         bg.scroll(-10, 0)
    #     if e.key == SDLK_RIGHT:
    #         bg.scroll(10, 0)

    boy.handle_event(e)

if __name__ == '__main__':
    gfw.start_main_module()

