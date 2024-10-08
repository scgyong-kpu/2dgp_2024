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
        for go in gfw.top().world.objects_at(scene.world.layer.ball):
            # if not isinstance(go, Ball): continue
            if not go.bounced: continue
            dx, dy = self.x - go.x, self.y - go.y
            if (-30 < dx and dx < 30) and (-50 < dy and dy < 50):
                # 충돌한 것으로 본다
                scene.world.remove(go)

    def handle_event(self, e):
        if e.type == SDL_KEYDOWN:
            if e.key == SDLK_LEFT:
                self.x -= 10
            elif e.key == SDLK_RIGHT:
                self.x += 10
            elif e.key == SDLK_SPACE:
                ball = Ball(self.x, self.y)
                scene = gfw.top()
                scene.world.append(ball)

    def __repr__(self):
        return 'Boy'
