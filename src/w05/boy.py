from pico2d import *
import random
import gfw

class Boy:
    def __init__(self):
        self.image = gfw.image.load('animation_sheet.png')
        self.frame = random.randint(0, 7)
        self.x, self.y = get_canvas_width() // 2, get_canvas_height() // 2
        self.action = 2 # 3=StandRight, 2=StandLeft, 1=RunRight, 0=RunLeft
    def draw(self):
        x = self.frame * 100
        y = self.action * 100
        self.image.clip_draw(x, y, 100, 100, self.x, self.y)
    def update(self):
        self.frame = (self.frame + 1) % 8

    def handle_event(self, e):
        if e.type == SDL_KEYDOWN:
            if e.key == SDLK_LEFT:
                self.x -= 10
            elif e.key == SDLK_RIGHT:
                self.x += 10
            elif e.key == SDLK_SPACE:
                self.action = (self.action + 1) % 4

    def __repr__(self):
        return 'Boy'
