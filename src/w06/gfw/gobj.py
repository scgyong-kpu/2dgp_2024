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

