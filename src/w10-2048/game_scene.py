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
    def __init__(self, n):
        fn = f'res/block_{n:05d}.png'
        super().__init__(fn, 0, 0, 10) # 10fps
        self.layer_index = world.layer.block

    def move_to(self, x, y):
        self.x = x * 120 + 80
        self.y = y * 120 + 80

    def remove(self):
        world.remove(self)

    def __del__(self):
        print(f'Removing {self}')

def generate_block():
    if board.is_full(): return

    block = NumBlock(random.choice([2, 4]))
    x, y = board.generate_block(block)
    block.move_to(x, y)

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

    if e.type == SDL_KEYDOWN:
        if e.key == SDLK_SPACE:
            generate_block()
        elif e.key == SDLK_LEFT:
            board.move_left()
        elif e.key == SDLK_RIGHT:
            board.move_right()
        elif e.key == SDLK_BACKSPACE:
            board.clear()

if __name__ == '__main__':
    gfw.start_main_module()

