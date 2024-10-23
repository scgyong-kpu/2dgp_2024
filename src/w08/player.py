from pico2d import * 
from gfw import *
import time

def make_rect(idx):
    x, y = idx % 100, idx // 100
    return (x * 272 + 67, y * 272 + 2, 138, 138)
    # return (x * 272 + 2, y * 272 + 2, 270, 270)

def make_rects(*idxs):
    return list(map(make_rect, idxs))

RECTS = [
    make_rects(400, 401, 402, 403),
    make_rects(507, 508),
    make_rects(501, 502, 503, 504),
    make_rects(509, 510),
]
STATE_RUNNING, STATE_JUMP, STATE_DOUBLE_JUMP, STATE_SLIDE = range(4)

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
        self.state = STATE_RUNNING
        self.src_rects = RECTS[self.state]

    def handle_event(self, e):
        if e.type == SDL_KEYDOWN and e.key == SDLK_SPACE:
            self.toggle_state()

    def toggle_state(self):
        self.state = (self.state + 1) % len(RECTS)
        self.src_rects = RECTS[self.state]

