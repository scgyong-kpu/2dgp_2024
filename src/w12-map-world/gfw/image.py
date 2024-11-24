from pico2d import *

_images = {}

def load(file):
    global _images
    if file in _images:
        return _images[file]

    image = load_image(file)
    _images[file] = image
    return image

def unload(file):
    global _images
    if file in _images:
        del _images[file]

class NinePatch:
    def __init__(self, image, l, b, r, t):
        self.image = image
        self.margins = l, b, r, t

    def draw(self, x, y, width, height):
        self.draw_to_origin(x - width // 2, y - height // 2, width, height)

    def draw_to_origin(self, left, bottom, width, height):
        l, b, r, t = self.margins
        iw, ih = self.image.w, self.image.h
        dr, dt = left + width - r, bottom + height - t
        scw, sch = iw - l - r, ih - l - r
        dcw, dch = width - l - r, height - l - r
        self.image.clip_draw_to_origin(0, 0, l, b, left, bottom) # left-bottom
        self.image.clip_draw_to_origin(iw - r, 0, r, b, dr, bottom) # right-bottom
        self.image.clip_draw_to_origin(0, ih - t, l, t, left, dt) # left-top
        self.image.clip_draw_to_origin(iw - r, ih - t, r, t, dr, dt) # right-top
        self.image.clip_draw_to_origin(l, 0, scw, b, left + l, bottom, dcw, b) # center-bottom
        self.image.clip_draw_to_origin(0, b, l, sch, left, bottom + b, l, dch) # left-center
        self.image.clip_draw_to_origin(iw - r, b, r, sch, dr, bottom + b, r, dch) # right-center
        self.image.clip_draw_to_origin(l, ih-t, scw, t, left + l, dt, dcw, t) # center-top
        self.image.clip_draw_to_origin(l, b, scw, sch, left + l, bottom + b, dcw, dch) # center-center

