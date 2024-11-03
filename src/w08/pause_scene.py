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
        e.key = SDLK_ESCAPE
        return False # pop one more scene

def draw():
    draw_centered_text(font, 'Press ESC to Resume', center_x, center_y + 30)
    draw_centered_text(font, 'Press Backspace to Exit', center_x, center_y - 20)

def update():
    pass

def get_text_extent(font, text):
    w, h = c_int(), c_int()
    TTF_SizeText(font.font, text.encode('utf-8'), ctypes.byref(w), ctypes.byref(h))
    return w.value, h.value

def draw_centered_text(font, text, x, y):
    tw, th = get_text_extent(font, text)
    tx = x - tw // 2
    ty = y - th // 2
    font.draw(tx, ty, text)

if __name__ == '__main__':
    gfw.start_main_module()


