from pico2d import * 
from gfw import *
import castle

import sys
self = sys.modules[__name__]

world = World(2)
transparent = True

msg = ''

def enter():
    global center_x, center_y
    center_x = get_canvas_width() // 2
    center_y = get_canvas_height() // 2

    global font
    font = gfw.font.load('res/ENCR10B.TTF')

    world.append(Background('res/trans_50b.png'), 0)
    world.append(Sprite('res/select_bg.png', center_x, center_y), 0)

    world.append(self, 1)

def set_result(life, max_life):
    global msg
    rate = min(3, 3 - int((max_life - life) / max_life * 3))
    if rate <= 0:
        msg = 'Game Over'
    else:
        msg = f'Cleard!! {"*" * rate} {life}/{max_life}'

def exit():
    world.clear()

life = 1000
set_result(life, life)

def handle_event(e):
    global life
    if e.type == SDL_KEYDOWN and e.key == SDLK_ESCAPE:
        gfw.pop()
        gfw.pop()
        return True
    if e.type == SDL_KEYDOWN and e.key == SDLK_SPACE:
        life += 100
        set_result(life, 1000)
    if e.type == SDL_KEYDOWN and e.key == SDLK_BACKSPACE:
        life -= 100
        set_result(life, 1000)

def draw():
    gfw.font.draw_centered_text(font, msg, center_x, center_y + 30, (63, 0, 0))
    gfw.font.draw_centered_text(font, 'Press ESC to Exit', center_x, center_y - 20, (0, 0, 63))

def update(): pass


if __name__ == '__main__':
    gfw.start_main_module()


