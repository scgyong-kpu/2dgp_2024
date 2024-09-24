from pico2d import *
import random

class Boy:
    def __init__(self):
        self.image = load_image('run_animation.png')
        self.frameIndex = random.randint(0, 7)
        self.x = random.randint(100, 700)
        self.y = random.randint(90, 500)
    def draw(self):
        x = self.frameIndex * 100
        self.image.clip_draw(x, 0, 100, 100, self.x, self.y)
    def update(self):
        self.frameIndex = (self.frameIndex + 1) % 8

