from gfw import *
from pico2d import *
import ingame_scene

import sys
self = sys.modules[__name__]

canvas_width = ingame_scene.canvas_width
canvas_height = ingame_scene.canvas_height

center_x = canvas_width // 2
center_y = canvas_height // 2
start_y = canvas_height * 2 // 3

world = World(2)

themes = [
    {
        "title": "Enemy",
        "folder": "enemy"
    },
    # {
    #     "title": "Another Title",
    #     "folder": "enemy"
    # }
]

def enter():
    world.append(Background('res/bg.png'), 0)
    world.append(self, 1)

    global font
    font = gfw.font.load('res/ENCR10B.TTF', 30)

    global nine_patch
    nine_patch = gfw.image.NinePatch(gfw.image.load('res/round_rect_9.png'), 24, 24, 24, 24)

def exit():
    world.clear()

def update(): pass
def draw(): 
    y = start_y
    for theme in themes:
        nine_patch.draw(center_x, y, 400, 80)
        gfw.font.draw_centered_text(font, theme["title"], center_x, y)
        y -= 100

def handle_event(e): pass
def pause(): pass
def resume(): pass

if __name__ == '__main__':
    gfw.start_main_module()

