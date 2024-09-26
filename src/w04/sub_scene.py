from pico2d import * 
import gfw
from random import randrange, uniform

# import main_scene
# main_scene 으로 전환하는 것이 아니고 나만 종료 (pop) 하면 된다.

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

game_objects = []

def enter():
    game_objects.append(Ball())

def exit():
    game_objects.clear()
    print('[sub.exit()]')

def pause():
    pass

def resume():
    pass

def handle_event(e):
    pass

if __name__ == '__main__':
    gfw.start_main_module()

