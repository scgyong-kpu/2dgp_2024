from pico2d import *
import random
import gfw_image
from ball import Ball
import main_scene

class Boy:
    def __init__(self):
        self.image = gfw_image.load('run_animation.png')
        self.frameIndex = random.randint(0, 7)
        self.x = random.randint(100, 700)
        self.y = random.randint(90, 500)
    def draw(self):
        x = self.frameIndex * 100
        self.image.clip_draw(x, 0, 100, 100, self.x, self.y)
    def update(self):
        self.frameIndex = (self.frameIndex + 1) % 8

    def handle_event(self, e):
        if e.type == SDL_KEYDOWN:
            if e.key == SDLK_LEFT:
                self.x -= 10
            elif e.key == SDLK_RIGHT:
                self.x += 10
            elif e.key == SDLK_SPACE:
                ball = Ball()
                main_scene.game_objects.append(ball)

''' 상호참조의 문제가 생긴다: 아래 메시지 중 circular import 에 주목하자.
Pico2d is prepared.
Traceback (most recent call last):
  File "D:/Lectures/2024_2/2dgp/git/src/w04/main_scene.py", line 6, in <module>
    from boy import Boy
  File "D:/Lectures/2024_2/2dgp/git/src/w04/boy.py", line 5, in <module>
    import main_scene
  File "D:/Lectures/2024_2/2dgp/git/src/w04/main_scene.py", line 6, in <module>
    from boy import Boy
ImportError: cannot import name 'Boy' from partially initialized module 'boy' (most likely due to a circular import) (D:/Lectures/2024_2/2dgp/git/src/w04/boy.py)
'''
