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
    SPEED_PPS = 3000
    def __init__(self, n):
        fn = f'res/block_{n:05d}.png'
        super().__init__(fn, 0, 0, 10) # 10fps
        self.layer_index = world.layer.block

    def move_to(self, x, y, animates=True):
        tx = x * 120 + 80
        ty = y * 120 + 80
        if animates:
            self.tx, self.ty = tx, ty
        else:
            self.x, self.y = tx, ty
            self.tx, self.ty = None, None

    def update(self):
        if self.tx is None: return
        dist = self.SPEED_PPS * gfw.frame_time
        x, y = self.x, self.y
        tx, ty = self.tx, self.ty
        if x < tx:
            x = min(x + dist, tx)
        elif x > tx:
            x = max(tx, x - dist)
        if y < ty:
            y = min(y + dist, ty)
        elif y > ty:
            y = max(ty, y - dist)

        self.x, self.y = x, y
        if (self.x, self.y) == (self.tx, self.ty):
            self.tx, self.ty = None, None

    def remove(self):
        world.remove(self)

    def __del__(self):
        print(f'Removing {self}')

def generate_block():
    if board.is_full(): return

    block = NumBlock(random.choice([2, 4]))
    x, y = board.generate_block(block)
    block.move_to(x, y, False)

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
        elif e.key == SDLK_UP:
            board.move_up()
        elif e.key == SDLK_DOWN:
            board.move_down()
        elif e.key == SDLK_BACKSPACE:
            board.clear()

if __name__ == '__main__':
    gfw.start_main_module()

