import time
from pico2d import *
import gfw

class Gauge:
    def __init__(self, fg_fname, bg_fname):
        self.fg = gfw.image.load(fg_fname)
        self.bg = gfw.image.load(bg_fname)
    def draw(self, x, y, width, rate):
        l = x - width // 2
        b = y - self.bg.h // 2
        self.draw_3(self.bg, l, b, width, 3)
        self.draw_3(self.fg, l, b, round(width * rate), 3)
    def draw_3(self, img, l, b, width, edge):
        img.clip_draw_to_origin(0, 0, edge, img.h, l, b, edge, img.h)
        img.clip_draw_to_origin(edge, 0, img.w - 2 * edge, img.h, l+edge, b, width - 2 * edge, img.h)
        img.clip_draw_to_origin(img.w - edge, 0, edge, img.h, l+width-edge, b, edge, img.h)

class Sprite:
    def __init__(self, filename, x, y):
        self.filename = filename
        self.image = gfw.image.load(filename)
        self.x, self.y = x, y
        self.width, self.height = self.image.w, self.image.h
    def draw(self):
        self.image.draw(self.x, self.y)
    def update(self):
        pass
    def get_bb(self):
        l = self.x - self.width // 2
        b = self.y - self.height // 2
        r = self.x + self.width // 2
        t = self.y + self.height // 2
        return l, b, r, t

    def __repr__(self):
        return f'{type(self).__name__}({self.filename})'

class AnimSprite(Sprite):
    def __init__(self, filename, x, y, fps, frame_count=0):
        super().__init__(filename, x, y)
        self.fps = fps
        if frame_count == 0: # 정사각형인 경우 0 을 주면 알아서 갯수를 세도록 한다
            frame_count = self.image.w // self.image.h

        self.width = self.image.w // frame_count
        self.frame_count = frame_count
        self.created_on = time.time()

    # elapsed time 을 구하기 위해 update() 에서 gfw.frame_time 을 누적하지 않는다
    # 그렇게 해도 되긴 하지만, 간단한 반복 애니메이션은 정확한 시간 누적이 필요한게 아니다
    # 오히려 AnimSprite 를 상속하는 객체가 super().update() 를 호출해야만 하는 부담이 생긴다
    def draw(self):
        elpased = time.time() - self.created_on
        index = round(elpased * self.fps) % self.frame_count
        self.image.clip_draw(index * self.width, 0, self.width, self.height, self.x, self.y)

class ScoreSprite(Sprite):
    def __init__(self, img_file, right, y):
        super().__init__(img_file, right, y)
        self.digit_width = self.image.w // 10
        self.width = self.digit_width
        self.score = 0
        self.display = 0
    def draw(self):
        x = self.x
        score = self.display
        while score > 0:
            digit = score % 10
            sx = digit * self.digit_width
            # print(type(sx), type(digit), type(self.digit_width))
            self.image.clip_draw(sx, 0, self.digit_width, self.image.h, x, self.y)
            x -= self.digit_width
            score //= 10
    def update(self):
        diff = self.score - self.display;
        if diff == 0: return
        if -10 < diff and diff < 0:
            self.display -= 1
        elif 0 < diff and diff < 10:
            self.display += 1
        else:
            self.display += diff // 10

class Background(Sprite):
    def __init__(self, filename):
        cw, ch = get_canvas_width(), get_canvas_height()
        super().__init__(filename, cw // 2, ch // 2)
        self.width = cw
        self.height = ch

    def draw(self):
        self.image.draw(self.x, self.y, self.width, self.height)

class VertFillBackground(Background):
    def __init__(self, filename, speed=0):
        super().__init__(filename)
        self.dest_height = self.image.h * get_canvas_width() // self.image.w
        self.speed = speed
        self.scroll = 0
    def update(self):
        self.scroll += self.speed * gfw.frame_time

    def draw(self):
        y = self.scroll % self.dest_height
        if y != 0: y -= self.dest_height
        max_y = get_canvas_height()
        while y < max_y:
            self.image.draw_to_origin(0, y, self.width, self.dest_height)
            y += self.dest_height

