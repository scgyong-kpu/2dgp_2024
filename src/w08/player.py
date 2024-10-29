from pico2d import * 
from gfw import *
import time

def make_rect(idx):
    x, y = idx % 100, idx // 100
    return (x * 272 + 2, y * 272 + 2, 270, 270)

def make_rects(*idxs):
    return list(map(make_rect, idxs))

STATES = [
    (make_rects(400, 401, 402, 403), (120,136)),
    (make_rects(507, 508), (120, 115)),
    (make_rects(501, 502, 503, 504), (120, 115)),
    (make_rects(509, 510), (160,70)),
]
STATE_RUNNING, STATE_JUMP, STATE_DOUBLE_JUMP, STATE_SLIDE, STATE_COUNT = range(5)

class Cookie(SheetSprite):
    GRAVITY = 3000
    JUMP_POWER = 1000
    def __init__(self):
        super().__init__('res/cookie.png', 160, 500, 10)
        self.running = True
        self.width, self.height = 270, 270
        self.set_state(STATE_RUNNING)
        self.floor_y = self.y
        self.dy = 0

    def handle_event(self, e):
        if e.type == SDL_KEYDOWN and e.key == SDLK_SPACE:
            self.jump()

    def update(self):
        self.y += self.dy * gfw.frame_time
        if self.state in (STATE_JUMP, STATE_DOUBLE_JUMP):
            self.dy -= self.GRAVITY * gfw.frame_time
            # if self.dy < 0 and self.y <= self.floor_y:
            #     self.y, self.dy = self.floor_y, 0
            #     self.set_state(STATE_RUNNING)

        _,foot,_,_ = self.get_bb()
        floor = self.get_floor(foot)
        if floor is not None:
            l,b,r,t = floor.get_bb()
            if self.state == STATE_RUNNING:
                if foot > t:
                    self.set_state(STATE_JUMP)
                    self.dy = 0
            else:
                # print('falling', t, foot)
                if self.dy < 0 and int(foot) <= t:
                    self.y += t - foot
                    self.set_state(STATE_RUNNING)
                    self.dy = 0

    def get_floor(self, foot):
        selected = None
        sel_top = 0
        x, y = self.x, self.y
        world = gfw.top().world
        for floor in world.objects_at(world.layer.floor):
            l,b,r,t = floor.get_bb()
            if x < l or x > r: continue
            mid = (b + t) // 2
            if foot < mid: continue
            if t > sel_top:
                selected = floor
                sel_top = t
        return selected

    def jump(self):
        if self.state == STATE_RUNNING:
            next_state = STATE_JUMP
        elif self.state == STATE_JUMP:
            next_state = STATE_DOUBLE_JUMP
        else:
            return
        self.dy = self.JUMP_POWER
        self.set_state(next_state)

    def set_state(self, state):
        self.state = state
        self.src_rects, (self.width, self.height) = STATES[self.state]

    def get_bb(self):
        foot = self.y - self.src_rects[0][3] // 2 # 높이의 절반이 발끝의 위치
        half_width = self.width // 2
        return (self.x - half_width, foot, self.x + half_width, foot + self.height)


