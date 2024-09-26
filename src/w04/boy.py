from pico2d import *
import random
from ball import Ball
import gfw

def init():
    global image, frameIndex, x, y
    image = gfw.image.load('run_animation.png')
    frameIndex = random.randint(0, 7)
    x = random.randint(100, 700)
    y = random.randint(90, 500)

def draw():
    src_x = frameIndex * 100
    image.clip_draw(src_x, 0, 100, 100, x, y)

def update():
    global frameIndex
    frameIndex = (frameIndex + 1) % 8

    scene = gfw.top()
    for go in gfw.top().world.objects_at(scene.world.layer.ball):
        # if not isinstance(go, Ball): continue
        if not go.bounced: continue
        dx, dy = x - go.x, y - go.y
        if (-30 < dx and dx < 30) and (-50 < dy and dy < 50):
            # 충돌한 것으로 본다
            scene.world.remove(go)

def handle_event(e):
    global x, y
    if e.type == SDL_KEYDOWN:
        if e.key == SDLK_LEFT:
            x -= 10
        elif e.key == SDLK_RIGHT:
            x += 10
        elif e.key == SDLK_SPACE:
            ball = Ball(x, y)
            scene = gfw.top()
            scene.world.append(ball)


