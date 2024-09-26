from pico2d import * 
import gfw_loop
from random import randrange, uniform

class Ball:
    def __init__(self):
        self.image = load_image('ball_41x41.png')
        self.x = randrange(100, 700)
        self.y = randrange(100, 500)
        self.dx = uniform(1.0, 2.0) * (1 if randrange(2) == 0 else -1)
        self.dy = uniform(1.0, 2.0) * (1 if randrange(2) == 0 else -1)
    def draw(self):
        self.image.draw(self.x, self.y)
    def update(self):
        self.x += self.dx
        self.y += self.dy
        l,t,r,b = 25,35,25,35
        if (self.dx < 0 and self.x < l) or (self.dx > 0 and self.x > get_canvas_width() - r):
            self.dx *= -1
        if (self.dy < 0 and self.y < t) or (self.dy > 0 and self.y > get_canvas_height() - b):
            self.dy *= -1


def enter():
    gfw_loop.game_objects.append(Ball())

def exit():
    pass

def handle_event(e):
    if e.type == SDL_KEYDOWN:
        if e.key == SDLK_LEFT:
            boy.x -= 10
        elif e.key == SDLK_RIGHT:
            boy.x += 10

if __name__ == '__main__':
    gfw_loop.start_main_module()

