from pico2d import * 
# SDL_*, SDLK_* 상수를 쓰려면 선언해야 한다

import gfw_loop
from grass import Grass
from boy import Boy

def enter():
  gfw_loop.game_objects.append(Grass())
  global boy
  boy = Boy()
  gfw_loop.game_objects.append(boy)

def handle_event(e):
  if e.type == SDL_KEYDOWN:
    if e.key == SDLK_LEFT:
      boy.x -= 10
    elif e.key == SDLK_RIGHT:
      boy.x += 10

gfw_loop.start(enter, handle_event)


