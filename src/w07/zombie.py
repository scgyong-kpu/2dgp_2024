import random
import time
import os
from pico2d import *
from gfw import *

class Zombie(AnimSprite):
    FPS = 12
    SCALE = 4
    def __init__(self):
        x, y = random.randrange(get_canvas_width()), random.randrange(get_canvas_height())
        super().__init__('res/zombiefiles/male/Idle (1).png', x, y, self.FPS, 1)
        self.images = load_image_series('res/zombiefiles/male/Idle (%d).png')
        self.frame_count = len(self.images)
    def draw(self):
        elpased = time.time() - self.created_on
        index = round(elpased * self.fps) % self.frame_count
        image = self.images[index]
        image.draw(self.x, self.y, self.width // self.SCALE, self.height // self.SCALE)

def load_image_series(fmt):
    images = []
    index = 1
    while True:
        fn = fmt % index
        if not os.path.isfile(fn):
            break
        images.append(gfw.image.load(fn))
        index += 1
    return images
