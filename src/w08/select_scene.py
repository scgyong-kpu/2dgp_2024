from gfw import *
from pico2d import *
import main_scene

import sys
self = sys.modules[__name__]

canvas_width = main_scene.canvas_width
canvas_height = main_scene.canvas_height

center_x = canvas_width // 2
center_y = canvas_height // 2
cookie_y = center_y - 60

world = World(2)

def enter():
    world.append(HorzFillBackground('res/cookie_run_bg_1.png'), 0)
    world.append(Sprite('res/cookie_run_title.png', center_x, center_y + 200), 0)
    world.append(Sprite('res/select_bg.png', center_x, cookie_y), 0)
    world.append(self, 1)

    global font
    font = gfw.font.load('res/CookieRun Regular.ttf')

    import json
    global cookies
    with open('res/cookies.json', 'r') as f:
        cookies = json.load(f)

    set_cookie_index(0)

filename = None
cookie_index = -1

def set_cookie_index(idx):
    global filename
    if filename is not None:
        gfw.image.unload(filename)

    global cookie_index, cookie_name
    cookie_index = idx
    cookie = cookies[cookie_index]
    filename = f'res/cookies/{cookie["id"]}_icon.png'
    cookie_name = cookie["name"]

    global image
    image = gfw.image.load(filename)

def exit():
    if filename is not None:
        gfw.image.unload(filename)

    # gfw.font.unload(font)

def update():
    pass

def draw():
    image.draw(center_x, cookie_y + 20)
    draw_centered_text(font, cookie_name, center_x, cookie_y - 50)

def handle_event(e):
    if e.type == SDL_KEYDOWN:
        if e.key == SDLK_LEFT:
            set_cookie_index((cookie_index - 1) % len(cookies))
        if e.key == SDLK_RIGHT:
            set_cookie_index((cookie_index + 1) % len(cookies))
        if e.key == SDLK_RETURN:
            main_scene.cookie_info = cookies[cookie_index]
            gfw.push(main_scene)

def pause(): pass
def resume(): pass

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

