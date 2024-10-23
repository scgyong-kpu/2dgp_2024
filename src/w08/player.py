from pico2d import * 
from gfw import *
import time

def make_rect(idx):
    x, y = idx % 16, idx // 16
    return (x * 272 + 67, y * 272 + 2, 138, 138)
    # return (x * 272 + 2, y * 272 + 2, 270, 270)

def make_rects(*idxs):
    return list(map(make_rect, idxs))

RECTS_RUN = make_rects(0x40, 0x41, 0x42, 0x43)
RECTS_JUMP = make_rects(0x57, 0x58)

class SheetSprite(AnimSprite):
    def __init__(self, fname, x, y, fps):
        super().__init__(fname, x, y, fps, 1)
        self.src_rects = []

    def draw(self):
        elpased = time.time() - self.created_on
        frame_count = len(self.src_rects)
        index = round(elpased * self.fps) % frame_count
        src_rect = self.src_rects[index]
        self.image.clip_draw(*src_rect, self.x, self.y)

class Cookie(SheetSprite):
    def __init__(self):
        super().__init__('res/cookie.png', 160, 160, 10)
        self.running = True
        self.width, self.height = 138, 138
        self.src_rects = RECTS_RUN

    def handle_event(self, e):
        if e.type == SDL_KEYDOWN and e.key == SDLK_SPACE:
            self.toggle_state()

    def toggle_state(self):
        self.running = not self.running
        self.src_rects = RECTS_RUN if self.running else RECTS_JUMP

