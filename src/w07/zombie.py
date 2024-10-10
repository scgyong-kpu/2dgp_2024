import random
import time
import os
from pico2d import *
from gfw import *

class Zombie(AnimSprite):
    FPS = 12
    SCALE = 4
    GENDERS = ['male', 'female']
    ACTIONS = ['Attack', 'Dead', 'Idle', 'Walk']
    def __init__(self):
        x, y = random.randrange(get_canvas_width()), random.randrange(get_canvas_height())
        super().__init__(None, x, y, self.FPS, 1)
        self.gender = random.choice(self.GENDERS)
        self.set_action('Idle') # loads images
        self.width = self.images[0].w // self.SCALE
        self.height = self.images[0].h // self.SCALE
        self.flip = random.choice(['', 'h'])
        self.time = 1
        self.action_index = 2
    def load_images(self):
        self.images = load_image_series(f'res/zombiefiles/{self.gender}/{self.action} (%d).png')
        self.frame_count = len(self.images)
    def set_action(self, action):
        self.action = action
        self.load_images()
    def draw(self):
        main_scene = gfw.top()
        screen_pos = main_scene.bg.to_screen(self.x, self.y)
        elpased = time.time() - self.created_on
        index = round(elpased * self.fps) % self.frame_count
        image = self.images[index]
        image.composite_draw(0, self.flip, *screen_pos, self.width, self.height)
    def update(self):
        self.time -= gfw.frame_time
        if self.time <= 0:
            self.time = random.uniform(2, 10)
            self.action_index = (self.action_index + 1) % len(self.ACTIONS)
            self.set_action(self.ACTIONS[self.action_index])

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
