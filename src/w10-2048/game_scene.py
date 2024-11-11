import random
from pico2d import * 
from gfw import *
from board import Board

world = World(['bg', 'block', 'ui'])

canvas_width = 520
canvas_height = 600
shows_bounding_box = True
shows_object_count = True

class NumBlock(AnimSprite):
    def __init__(self, x, y, n):
        fn = f'res/block_{n:05d}.png'
        super().__init__(fn, x * 120 + 80, y * 120 + 80, 10) # 10fps
        self.layer_index = world.layer.block

def generate_block():
    if board.is_full(): return
    
    block = random.choice([2, 4])
    x, y = board.generate_block(block)

    block = NumBlock(x, y, block)
    world.append(block)

def enter():
    world.append(Background('res/FF9F49.png'), world.layer.bg)

    global board
    board = Board()

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

    if e.type == SDL_KEYDOWN and e.key == SDLK_SPACE:
        generate_block()

if __name__ == '__main__':
    gfw.start_main_module()

