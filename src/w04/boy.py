from pico2d import *
import random
from ball import Ball
import gfw

class Boy:
    def __init__(self):
        self.image = gfw.image.load('run_animation.png')
        self.frameIndex = random.randint(0, 7)
        self.x = random.randint(100, 700)
        self.y = random.randint(90, 500)
    def draw(self):
        x = self.frameIndex * 100
        self.image.clip_draw(x, 0, 100, 100, self.x, self.y)
    def update(self):
        self.frameIndex = (self.frameIndex + 1) % 8

        scene = gfw.top()
        for go in gfw.top().world.objects_at(1):
            # if not isinstance(go, Ball): continue
            if not go.bounced: continue
            dx, dy = self.x - go.x, self.y - go.y
            if (-30 < dx and dx < 30) and (-50 < dy and dy < 50):
                # 충돌한 것으로 본다
                scene.world.remove(go) # 이것으로 충분할까?


    def handle_event(self, e):
        if e.type == SDL_KEYDOWN:
            if e.key == SDLK_LEFT:
                self.x -= 10
            elif e.key == SDLK_RIGHT:
                self.x += 10
            elif e.key == SDLK_SPACE:
                ball = Ball(self.x, self.y)
                scene = gfw.top()
                scene.world.append(ball, 1) # layer_index 가 1 인걸 기억할수 있을까?


'''
Pico2d is prepared.
current_scene=<module '__main__' from 'D://Lectures//2024_2//2dgp//git//src//w04//main_scene.py'>
Traceback (most recent call last):
  File "D:/Lectures/2024_2/2dgp/git/src/w04/main_scene.py", line 38, in <module>
    gfw.start_main_module()
  File "D:/Lectures/2024_2/2dgp/git/src/w04/gfw.py", line 45, in start_main_module
    start(scene)
  File "D:/Lectures/2024_2/2dgp/git/src/w04/gfw.py", line 16, in start
    stack[-1].world.update()
  File "D:/Lectures/2024_2/2dgp/git/src/w04/gfw_world.py", line 17, in update
    go.update()
  File "D:/Lectures/2024_2/2dgp/git/src/w04/boy.py", line 21, in update
    if not go.bounced: continue
AttributeError: 'Boy' object has no attribute 'bounced'
'''
