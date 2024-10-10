import random
import time
import os
from pico2d import *
from gfw import *

class Zombie(AnimSprite):
    FPS = 12
    SCALE = 4
    ACTIONS = ['Attack', 'Dead', 'Idle', 'Walk']
    def __init__(self):
        x, y = random.randrange(get_canvas_width()), random.randrange(get_canvas_height())
        super().__init__(None, x, y, self.FPS, 1)
        gender = random.choice(['male', 'female'])
        action = random.choice(self.ACTIONS)
        self.images = load_image_series(f'res/zombiefiles/{gender}/{action} (%d).png')
        self.width = self.images[0].w // self.SCALE
        self.height = self.images[0].h // self.SCALE
        self.frame_count = len(self.images)
        self.flip = random.choice(['', 'h'])
    def draw(self):
        main_scene = gfw.top()
        print(main_scene.bg)
        elpased = time.time() - self.created_on
        index = round(elpased * self.fps) % self.frame_count
        image = self.images[index]
        image.composite_draw(0, self.flip, self.x, self.y, self.width, self.height)
    def get_bb(self):
        half_width  = self.width * 9 // 20
        half_height = self.height * 9 // 20
        l = self.x - half_width
        b = self.y - half_height
        r = self.x + half_width
        t = self.y + half_width
        return l, b, r, t

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
