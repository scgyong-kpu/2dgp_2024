from pico2d import *
import random
import gfw

class Boy(gfw.Sprite):
    def __init__(self):
        super().__init__('res/animation_sheet.png', get_canvas_width()//2, get_canvas_height()//2)
        self.time = 0 # age in seconds
        self.frame = 0
        self.dx, self.dy = 0, 0
        self.speed = 200
        self.action = 3 # 3=StandRight, 2=StandLeft, 1=RunRight, 0=RunLeft
        self.mag = 1
        self.target = None

    def draw(self):
        x = self.frame * 100
        y = self.action * 100
        screen_pos = self.bg.to_screen(self.x, self.y)
        self.image.clip_draw(x, y, 100, 100, *screen_pos)

    def update(self):
        self.time += gfw.frame_time
        fps, frame_count = 10, 8
        self.frame = round(self.time * fps) % frame_count
        self.x += self.dx * self.speed * self.mag * gfw.frame_time
        self.y += self.dy * self.speed * self.mag * gfw.frame_time
        self.x = clamp(self.bg.margin, self.x, self.bg.total_width() - self.bg.margin)
        self.y = clamp(self.bg.margin, self.y, self.bg.total_height() - self.bg.margin)
        # print(f'{self.y=}, {self.bg.total_height() - self.bg.margin=}')
        if self.target is not None:
            tx, ty = self.target
            if (self.dx > 0 and self.x >= tx) or (self.dx < 0 and self.x <= tx):
                self.x, self.dx = tx, 0
            if (self.dy > 0 and self.y >= ty) or (self.dy < 0 and self.y <= ty):
                self.y, self.dy = ty, 0
            if self.dx == 0 and self.dy == 0:
                self.target = None
                self.adjust_action()
        self.bg.show(self.x, self.y)

    def adjust_delta(self, x, y):
        if self.target is not None:
            self.dx, self.dy = 0, 0
            self.target = None
        self.dx += x
        self.dy += y

    def set_target(self, mx, my):
        tx, ty = self.bg.from_screen(mx, my)
        if self.x == tx and self.y == ty:
            self.target = None
            self.dx, self.dy = 0, 0
            return
        self.target = tx, ty
        rad = math.atan2(ty - self.y, tx - self.x)
        self.dx, self.dy = math.cos(rad), math.sin(rad)

    def handle_event(self, e):
        dx, dy = self.dx, self.dy
        if e.type == SDL_KEYDOWN:
            if e.key == SDLK_LEFT:    self.adjust_delta(-1, 0)
            elif e.key == SDLK_RIGHT: self.adjust_delta(1, 0)
            elif e.key == SDLK_DOWN:  self.adjust_delta(0, -1)
            elif e.key == SDLK_UP:    self.adjust_delta(0, 1)
            elif e.key == SDLK_LSHIFT:
                self.mag *= 2

        elif e.type == SDL_KEYUP:
            if e.key == SDLK_LEFT:    self.adjust_delta(1, 0)
            elif e.key == SDLK_RIGHT: self.adjust_delta(-1, 0)
            elif e.key == SDLK_DOWN:  self.adjust_delta(0, 1)
            elif e.key == SDLK_UP:    self.adjust_delta(0, -1)
            elif e.key == SDLK_LSHIFT:
                self.mag //= 2

        elif e.type == SDL_MOUSEBUTTONDOWN:
            self.set_target(e.x, get_canvas_height() - e.y - 1)
        elif e.type == SDL_MOUSEMOTION:
            if self.target is not None:
                self.set_target(e.x, get_canvas_height() - e.y - 1)

        # print(f'({dx=}, {dy=}) != ({self.dx=}, {self.dy=})')
        if (dx, dy) != (self.dx, self.dy):
            self.adjust_action()

    def adjust_action(self):
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

    def get_bb(self):
        hw, hh = 20, 34
        return self.x - hw, self.y - hh, self.x + hw, self.y + hh

    def __repr__(self):
        return 'Boy'
