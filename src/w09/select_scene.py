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
    def __init__(self, nine_patch, font, title, x, y, width, height, on_click):
        super().__init__(None, x, y)
        self.bg = nine_patch
        self.width, self.height = width, height
        self.title = title
        self.font = font
        self._on_click = on_click

    def draw(self):
        self.bg.draw(self.x, self.y, self.width, self.height)
        gfw.font.draw_centered_text(self.font, self.title, self.x, self.y)

    def handle_event(self, e):
        if not self.contains_xy(*gfw.mouse_xy(e)): return False
        # print(e.type, self.title)
        if e.type == SDL_MOUSEBUTTONDOWN and e.button == SDL_BUTTON_LEFT:
            self._on_click()


class ThemeButton(Button):
    @staticmethod
    def load():
        ThemeButton.nine_patch = gfw.image.NinePatch(gfw.image.load('res/round_rect_9.png'), 24, 24, 24, 24)
        ThemeButton.font = gfw.font.load('res/ENCR10B.TTF', 30)

    def __init__(self, theme, x, y):
        super().__init__(self.nine_patch, self.font, theme['title'], x, y, 400, 80, lambda: print('Clicked:', theme['title']))

def enter():
    world.append(Background('res/bg.png'), 0)

    # global font
    # font = gfw.font.load('res/ENCR10B.TTF', 30)

    ThemeButton.load()

    import json
    global themes
    with open('res/themes.json', 'r') as f:
        themes = json.load(f)

    y = start_y
    for theme in themes:
        world.append(ThemeButton(theme, center_x, y), 1)
        y -= 100

def exit():
    world.clear()

def update(): pass
def draw(): pass
def handle_event(e): 
    if e.type in [ SDL_MOUSEMOTION, SDL_MOUSEBUTTONDOWN, SDL_MOUSEBUTTONUP ]:
        for btn in world.objects_at(1):
            if btn.handle_event(e):
                return True
def pause(): pass
def resume(): pass

if __name__ == '__main__':
    gfw.start_main_module()

