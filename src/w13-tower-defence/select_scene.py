from pico2d import * 
from gfw import *
import game_scene

canvas_width = game_scene.canvas_width
canvas_height = game_scene.canvas_height

import sys
self = sys.modules[__name__]

world = gfw.World(['bg', 'button'])

STAGE_INFOS = {
    1: ('Stage 1', (canvas_width // 2, canvas_height // 2 + 130, 500, 100)), 
    2: ('Stage 2', (canvas_width // 2, canvas_height // 2,       500, 100)), 
    3: ('Stage 3', (canvas_width // 2, canvas_height // 2 - 130, 500, 100)), 
}

class StageButton(Button):
    @staticmethod
    def load():
        StageButton.np_normal = gfw.image.NinePatch(gfw.image.load('res/btn_bg_normal_9.png'), 36,36,35,35)
        StageButton.np_over = gfw.image.NinePatch(gfw.image.load('res/btn_bg_over_9.png'), 36,36,35,35)
        StageButton.font = gfw.font.load('res/ENCR10B.TTF', 30)

    def __init__(self, stage):
        if not hasattr(StageButton, 'font'):
            StageButton.load()
        title, rect = STAGE_INFOS[stage]
        super().__init__(self.np_normal, self.np_over, self.font, title, *rect, self.on_click)
        self.stage = stage

    def on_click(self):
        game_scene.stage = self.stage
        gfw.push(game_scene)
        self.bg = self.bg_n

def enter():
    world.append(self, world.layer.bg)
    global tile_img
    tile_img = gfw.image.load('res/select_bg_tile.png')
    for stage in range(1, 3+1):
        world.append(StageButton(stage), world.layer.button)
def exit():
    world.clear()
def update(): pass
def draw():
    tilesize = 48
    for y in range(0, canvas_height, tilesize):
        for x in range(0, canvas_width, tilesize):
            tile_img.draw_to_origin(x, y, tilesize, tilesize)
def pause():
    print('[select.pause()]')
def resume():
    print('[select.resume()]')
def handle_event(e):
    if e.type in [ SDL_MOUSEMOTION, SDL_MOUSEBUTTONDOWN, SDL_MOUSEBUTTONUP ]:
        for btn in world.objects_at(1):
            if btn.handle_event(e):
                return True

if __name__ == '__main__':
    gfw.start_main_module()


