import json
import math
from gfw import *

class TestScene:
    def enter(self):
        self.world = World()
        self.map_bg = MapBackground('res/earth.json', fitsWidth=True)
        self.world.append(self.map_bg, 0)
        # self.shows_bounding_box = True
    def exit(self): pass
    def handle_event(self, e):
        if e.type == SDL_KEYDOWN and e.key == SDLK_1:
            print(self.world.objects)
        if e.type == SDL_MOUSEMOTION:
            # dx = get_canvas_width() // 2 - e.x
            dx = 0
            dy = get_canvas_height() // 2 - e.y

            self.map_bg.set_scroll_speed(dx, dy)

if __name__ == '__main__':
    scene = TestScene()
    gfw.start(scene)


