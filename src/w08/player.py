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
    (make_rects(500), (110,126)),
]
STATE_RUNNING, STATE_JUMP, STATE_DOUBLE_JUMP, STATE_SLIDE, STATE_FALLING, STATE_COUNT = range(6)

RECTS_RUNNING_MAGNIFIED = make_rects(404, 405, 406, 407)

class Cookie(SheetSprite):
    GRAVITY = 3000
    JUMP_POWER = 1000
    def __init__(self):
        super().__init__('res/cookie.png', 160, 500, 10)
        self.running = True
        self.width, self.height = 270, 270
        self.floor_y = self.y
        self.dy = 0
        self.mag = 1
        self.mag_speed = 0
        self.set_state(STATE_RUNNING)

    def handle_event(self, e):
        if e.type == SDL_KEYDOWN:
            if e.key == SDLK_SPACE or e.key == SDLK_UP:
                self.jump()
            elif e.key == SDLK_DOWN:
                self.move_down_from_floor()
            elif e.key == SDLK_RETURN:
                self.slide(True)
            elif e.key == SDLK_m:
                self.toggle_mag()
        elif e.type == SDL_KEYUP:
            if e.key == SDLK_RETURN:
                self.slide(False)

    def slide(self, starts):
        if starts:
            if self.state == STATE_RUNNING:
                self.set_state(STATE_SLIDE)
        else:
            if self.state == STATE_SLIDE:
                self.set_state(STATE_RUNNING)

    def toggle_mag(self):
        self.mag_speed = 1 if self.mag == 1 else -1
        if self.state == STATE_RUNNING:
            self.src_rects = RECTS_RUNNING_MAGNIFIED

    def update_mag(self):
        if self.mag_speed == 0: return
        _,foot1,_,_ = self.get_bb()

        self.mag += self.mag_speed * gfw.frame_time
        if self.mag > 2:
            self.mag = 2
            self.mag_speed = 0
        elif self.mag < 1:
            self.mag = 1
            self.mag_speed = 0
            if self.state == STATE_RUNNING:
                self.src_rects = STATES[STATE_RUNNING][0]

        _,foot2,_,_ = self.get_bb()
        self.y += foot1 - foot2

    def update(self):
        self.update_mag()

        _,foot,_,_ = self.get_bb()
        floor = self.get_floor(foot)
        t = 0 if floor is None else floor.get_bb()[3]

        if self.state in (STATE_JUMP, STATE_DOUBLE_JUMP, STATE_FALLING):
            self.dy -= self.GRAVITY * gfw.frame_time
            new_foot = foot + self.dy * gfw.frame_time
            if self.dy < 0 and new_foot <= t:
                self.y += t - foot # y 는 현재 foot 에서 도착지점 t 까지의 거리만 보정해주면 된다.
                self.set_state(STATE_RUNNING)
                self.dy = 0
            else:
                self.y += self.dy * gfw.frame_time

        if self.state in (STATE_RUNNING, STATE_SLIDE):
            if foot > t:
                # print(f'{foot=:.1f} {t=}')
                self.set_state(STATE_FALLING)
                self.dy = 0

        self.check_collision()

    def get_floor(self, foot):
        selected = None
        sel_top = 0
        x, y = self.x, self.y
        world = gfw.top().world
        for floor in world.objects_at(world.layer.floor):
            l,b,r,t = floor.get_bb()
            if x < l or x > r: continue
            # print(f"{foot=:.1f} {t=:.1f} {sel_top=:.1f} {floor}")
            if foot < t: continue
            if t > sel_top:
                selected = floor
                sel_top = t
        return selected

    def move_down_from_floor(self):
        _,foot,_,_ = self.get_bb()
        floor = self.get_floor(foot)
        if floor is None or not floor.canPassThrough():
            return
        if self.state != STATE_RUNNING: return
        self.y -= 1

    def check_collision(self):
        world = gfw.top().world
        items = world.objects_at(world.layer.item)
        for item in items:
            if collides_box(self, item):
                world.remove(item)

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
        # print(f'{state=}')
        self.state = state
        self.src_rects, (self.width, self.height) = STATES[self.state]
        self.frame_count = len(self.src_rects)
        if state == STATE_RUNNING and self.mag != 1:
            self.src_rects = RECTS_RUNNING_MAGNIFIED

    def get_bb(self):
        foot = self.y - self.src_rects[0][3] // 2 * self.mag 
        half_width = self.width // 2 * self.mag
        return (self.x - half_width, foot, self.x + half_width, foot + self.height * self.mag)

    def draw(self):
        index = self.get_anim_index()
        l, b, w, h = self.src_rects[index]
        self.image.clip_draw(l, b, w, h, self.x, self.y, self.mag * w, self.mag * h)

