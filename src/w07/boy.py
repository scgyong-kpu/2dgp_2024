from pico2d import *
import random
import gfw

class Boy:
    def __init__(self):
        self.image = gfw.image.load('res/animation_sheet.png')
        self.time = 0 # age in seconds
        self.frame = 0
        self.x, self.y = get_canvas_width()//2, get_canvas_height()//2
        self.dx, self.dy = 0, 0
        self.speed = 200
        self.action = 3 # 3=StandRight, 2=StandLeft, 1=RunRight, 0=RunLeft

    def draw(self):
        x = self.frame * 100
        y = self.action * 100
        self.image.clip_draw(x, y, 100, 100, self.x, self.y)

    def update(self):
        self.time += gfw.frame_time
        fps, frame_count = 10, 8
        self.frame = round(self.time * fps) % frame_count
        self.x += self.dx * self.speed * gfw.frame_time
        self.y += self.dy * self.speed * gfw.frame_time

    def handle_event(self, e):
        dx, dy = self.dx, self.dy
        if e.type == SDL_KEYDOWN:
            if e.key == SDLK_LEFT:
                self.dx -= 1
            elif e.key == SDLK_RIGHT:
                self.dx += 1
            elif e.key == SDLK_DOWN:
                self.dy -= 1
            elif e.key == SDLK_UP:
                self.dy += 1

        elif e.type == SDL_KEYUP:
            if e.key == SDLK_LEFT:
                self.dx += 1
            elif e.key == SDLK_RIGHT:
                self.dx -= 1
            elif e.key == SDLK_DOWN:
                self.dy += 1
            elif e.key == SDLK_UP:
                self.dy -= 1

        if (dx, dy) != (self.dx, self.dy):
            if self.dx > 0:
                self.action = 1
            elif self.dx < 0:
                self.action = 0
            else:
                if self.dy != 0: 
                    if self.action >= 2:
                        self.action -= 2
                else:
                    if self.action < 2:
                        self.action += 2

    def __repr__(self):
        return 'Boy'
