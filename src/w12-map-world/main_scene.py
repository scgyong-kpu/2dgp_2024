from pico2d import * 
from gfw import *
from boy import Boy

world = gfw.World(['bg', 'enemy', 'item', 'player', 'ui', 'controller'])

canvas_width = 1280
canvas_height = 720
shows_bounding_box = True
shows_object_count = True

def enter():
    world.bg = MapBackground('res/desert.tmj')
    world.append(world.bg, world.layer.bg)
    global player
    player = Boy()
    player.bg = world.bg
    world.append(player, world.layer.player)

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

if __name__ == '__main__':
    gfw.start_main_module()

