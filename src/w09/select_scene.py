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

class Button(Sprite):
    def __init__(self, nine_patch, title, x, y, width, height):
        super().__init__(None, x, y)
        self.bg = nine_patch
        self.width, self.height = width, height
        self.title = title
        self.font = gfw.font.load('res/ENCR10B.TTF', 30)

    def draw(self):
        self.bg.draw(self.x, self.y, self.width, self.height)
        gfw.font.draw_centered_text(self.font, self.title, self.x, self.y)

def enter():
    world.append(Background('res/bg.png'), 0)

    # global font
    # font = gfw.font.load('res/ENCR10B.TTF', 30)

    global nine_patch
    nine_patch = gfw.image.NinePatch(gfw.image.load('res/round_rect_9.png'), 24, 24, 24, 24)

    import json
    global themes
    with open('res/themes.json', 'r') as f:
        themes = json.load(f)

    y = start_y
    for theme in themes:
        world.append(Button(nine_patch, theme["title"], center_x, y, 400, 80), 1)
        y -= 100

def exit():
    world.clear()

def update(): pass
def draw(): pass
def handle_event(e): pass
def pause(): pass
def resume(): pass

if __name__ == '__main__':
    gfw.start_main_module()

