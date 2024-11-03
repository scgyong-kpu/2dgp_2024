from pico2d import * 
from gfw import *

world = World(['bg', 'card'])

canvas_width = 960
canvas_height = 540
shows_bounding_box = False #True
shows_object_count = True

center_x = canvas_width // 2
center_y = canvas_height // 2

def card_position(x, y):
    return (x + 1) * 120 - 30, (y + 1) * 120 - 28

class Card(AnimSprite):
    def __init__(self, x, y, index):
        super().__init__(f'res/f_{index:02d}.png', *card_position(x, y), 10)
        self.index = index

def enter():
    world.append(Background('res/bg_andromeda.png'), world.layer.bg)
    index = 0
    for y in range(4):
        for x in range(5):
            world.append(Card(x, y, index // 2 + 1), world.layer.card)
            index += 1

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

