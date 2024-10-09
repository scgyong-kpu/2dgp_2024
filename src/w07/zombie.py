import random
import time
from pico2d import *
from gfw import *

class Zombie(AnimSprite):
    FPS = 12
    SCALE = 4
    def __init__(self):
        x, y = random.randrange(get_canvas_width()), random.randrange(get_canvas_height())
        super().__init__('res/zombiefiles/male/Idle (1).png', x, y, self.FPS, 1)
        self.frame_count = 15
    def draw(self):
        elpased = time.time() - self.created_on
        index = round(elpased * self.fps) % self.frame_count
        file = 'res/zombiefiles/male/Idle (%d).png' % (index + 1)
        image = gfw.image.load(file)
        image.draw(self.x, self.y, self.width // self.SCALE, self.height // self.SCALE)
