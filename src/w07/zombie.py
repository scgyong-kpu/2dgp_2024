import random
import time
import os
from pico2d import *
from gfw import *

class Idle:
    def __init__(self):
        self.name = 'Idle'
    def update(self, zombie):
        pass
    def draw(self, zombie):
        pass
class Walk:
    def __init__(self):
        self.name = 'Walk'
    def update(self, zombie):
        pass
    def draw(self, zombie):
        pass
class Attack:
    def __init__(self):
        self.name = 'Attack'
    def update(self, zombie):
        zombie.x += random.uniform(-30, 30) * gfw.frame_time
        zombie.y += random.uniform(-30, 30) * gfw.frame_time
        # return False
    def draw(self, zombie):
        pass
class Dead:
    def __init__(self):
        self.name = 'Dead'
    def enter(self, zombie):
        zombie.time = 0
    def update(self, zombie):
        zombie.time += gfw.frame_time
        if zombie.time > 2:
            world = gfw.top().world
            world.remove(zombie, world.layer.zombie)
        return True
    def draw(self, zombie):
        main_scene = gfw.top()
        screen_pos = main_scene.bg.to_screen(zombie.x, zombie.y)
        index = min(round(zombie.time * zombie.fps), len(zombie.images) - 1)
        image = zombie.images[index]
        image.composite_draw(0, zombie.flip, *screen_pos, zombie.width, zombie.height)
        return True

class Zombie(AnimSprite):
    FPS = 12
    SCALE = 4
    GENDERS = ['male', 'female']
    STATES = [Idle(), Walk(), Attack(), Dead()]
    def __init__(self):
        x, y = random.randrange(get_canvas_width()), random.randrange(get_canvas_height())
        super().__init__(None, x, y, self.FPS, 1)
        self.gender = random.choice(self.GENDERS)
        self.set_state(0) # loads images
        self.width = self.images[0].w // self.SCALE
        self.height = self.images[0].h // self.SCALE
        self.flip = random.choice(['', 'h'])
        self.time = 1
    def load_images(self):
        self.images = load_image_series(f'res/zombiefiles/{self.gender}/{self.action} (%d).png')
        self.frame_count = len(self.images)
    def set_state(self, state_index):
        self.state_index = state_index
        self.state = self.STATES[state_index]
        self.action = self.state.name
        self.load_images()
        if hasattr(self.state, 'enter'):
            self.state.enter(self)
    def draw(self):
        if self.state.draw(self):
            return
        main_scene = gfw.top()
        screen_pos = main_scene.bg.to_screen(self.x, self.y)
        elpased = time.time() - self.created_on
        index = round(elpased * self.fps) % self.frame_count
        image = self.images[index]
        image.composite_draw(0, self.flip, *screen_pos, self.width, self.height)
    def update(self):
        if self.state.update(self):
            return
        self.time -= gfw.frame_time
        if self.time <= 0:
            self.time = random.uniform(2, 10)
            self.set_state((self.state_index + 1) % len(self.STATES))

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
