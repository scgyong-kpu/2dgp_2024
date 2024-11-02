from gfw import *
from pico2d import *
import main_scene

canvas_width = main_scene.canvas_width
canvas_height = main_scene.canvas_height

center_x = canvas_width // 2
center_y = canvas_height // 2

world = World(2)

def enter():
    world.append(HorzFillBackground('res/cookie_run_bg_1.png'), 0)
    world.append(Sprite('res/cookie_run_title.png', center_x, center_y + 200), 0)
    world.append(Sprite('res/select_bg.png', center_x, center_y - 60), 0)

def exit():
    pass

def handle_event(e):
    pass

if __name__ == '__main__':
    gfw.start_main_module()

