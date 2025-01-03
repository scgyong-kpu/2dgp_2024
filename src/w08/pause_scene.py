from pico2d import * 
from gfw import *

import sys
self = sys.modules[__name__]

world = World(2)
transparent = True

def enter():
    global center_x, center_y
    center_x = get_canvas_width() // 2
    center_y = get_canvas_height() // 2

    global font
    font = gfw.font.load('res/CookieRun Regular.ttf')

    world.append(Background('res/trans_50b.png'), 0)
    world.append(Sprite('res/select_bg.png', center_x, center_y), 0)

    world.append(self, 1)

def exit():
    world.clear()

def handle_event(e):
    if e.type == SDL_KEYDOWN and e.key == SDLK_BACKSPACE:
        gfw.pop()
        gfw.pop()
        return True

def draw():
    gfw.font.draw_centered_text(font, 'Press ESC to Resume',     center_x, center_y + 30, (63, 0, 0))
    gfw.font.draw_centered_text(font, 'Press Backspace to Exit', center_x, center_y - 20, (0, 0, 63))

def update():
    pass

if __name__ == '__main__':
    gfw.start_main_module()


