import random
import time
import os
from pico2d import *
from gfw import *


class SubState:
    def __init__(self, **funcs):
        self.funcs = funcs
    def draw(self):
        self.funcs['draw']()
    def update(self):
        self.funcs['update']()
    def enter(self):
        if 'enter' in self.funcs:
            self.funcs['enter']()
    def exit(self):
        if 'exit' in self.funcs:
            self.funcs['exit']()

class Zombie(AnimSprite):
    FPS = 12
    SCALE = 4
    GENDERS = ['male', 'female']
    NEXTS = {'Idle':'Walk', 'Walk':'Attack', 'Attack':'Dead'}
    def __init__(self):
        x, y = random.randrange(get_canvas_width()), random.randrange(get_canvas_height())
        super().__init__(None, x, y, self.FPS, 1)
        self.gender = random.choice(self.GENDERS)
        self.states = {
            'Idle': SubState(draw=self.draw_normal, update=self.update_normal),
            'Walk': SubState(draw=self.draw_normal, update=self.update_normal),
            'Attack': SubState(draw=self.draw_normal, update=self.update_attack),
            'Dead': SubState(draw=self.draw_dead, update=self.update_dead, enter=self.enter_dead),
        }
        self.set_state('Idle')
        self.width = self.images[0].w // self.SCALE
        self.height = self.images[0].h // self.SCALE
        self.flip = random.choice(['', 'h'])
        self.time = 1
    def load_images(self):
        self.images = load_image_series(f'res/zombiefiles/{self.gender}/{self.action} (%d).png')
        self.frame_count = len(self.images)
    def set_state(self, state_name):
        self.state = self.states[state_name]
        self.action = state_name
        self.load_images()
        self.state.enter()
    def draw(self):
        self.state.draw()
    def draw_normal(self):
        main_scene = gfw.top()
        screen_pos = main_scene.bg.to_screen(self.x, self.y)
        elpased = time.time() - self.created_on
        index = round(elpased * self.fps) % self.frame_count
        image = self.images[index]
        image.composite_draw(0, self.flip, *screen_pos, self.width, self.height)
    def update(self):
        self.state.update()
    def update_normal(self):
        self.time -= gfw.frame_time
        if self.time <= 0:
            self.time = random.uniform(2, 10)
            next_state = self.NEXTS[self.action]
            self.set_state(next_state)
    def update_attack(self):
        self.x += random.uniform(-30, 30) * gfw.frame_time
        self.y += random.uniform(-30, 30) * gfw.frame_time
        self.update_normal()
    def enter_dead(self):
        self.time = 0
    def update_dead(self):
        self.time += gfw.frame_time
        if self.time > 2:
            world = gfw.top().world
            world.remove(self, world.layer.zombie)
    def draw_dead(self):
        main_scene = gfw.top()
        screen_pos = main_scene.bg.to_screen(self.x, self.y)
        index = min(round(self.time * self.fps), len(self.images) - 1)
        image = self.images[index]
        image.composite_draw(0, self.flip, *screen_pos, self.width, self.height)

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
