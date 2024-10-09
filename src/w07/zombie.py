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
        gender = random.choice(['male', 'female'])
        action = random.choice(['Idle', 'Walk', 'Attack', 'Dead'])
        self.images = load_image_series(f'res/zombiefiles/{gender}/{action} (%d).png')
        self.frame_count = len(self.images)
        self.flip = random.choice(['', 'h'])
    def draw(self):
        elpased = time.time() - self.created_on
        index = round(elpased * self.fps) % self.frame_count
        image = self.images[index]
        image.composite_draw(0, self.flip, self.x, self.y, self.width // self.SCALE, self.height // self.SCALE)

def load_image_series(fmt):
    images = []
    index = 1
    while True:
        fn = fmt % index
        if not os.path.isfile(fn):
            break
        images.append(gfw.image.load(fn))
        index += 1
    # print(f'{fmt} {len(images)} images')
    return images
