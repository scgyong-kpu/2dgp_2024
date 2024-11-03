from pico2d import * 
from gfw import *

world = World(2)

def enter():
    center_x = get_canvas_width() // 2
    center_y = get_canvas_height() // 2

    world.append(Background('res/trans_50b.png'), 0)
    world.append(Sprite('res/select_bg.png', center_x, center_y), 0)

def exit():
    world.clear()

def handle_event(e):
    pass

if __name__ == '__main__':
    gfw.start_main_module()


