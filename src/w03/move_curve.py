from pico2d import *
import math
import random

def reset():
  global x, y
  x, y = 100, 65

func_tables = [
  (reset, reset),
]

def handle_events():
  global running, update
  for e in get_events():
    if e.type == SDL_QUIT:
      running = False
    elif e.type == SDL_MOUSEMOTION:
      global mouse_x, mouse_y
      mouse_x, mouse_y = e.x, get_canvas_height() - e.y - 1
    elif e.type == SDL_KEYDOWN:
      if e.key == SDLK_ESCAPE:
        running = False
      else:
        idx = e.key - SDLK_0
        if idx >= 0 and idx < len(func_tables):
          reset()
          init_func, update = func_tables[idx]
          print(f'{e.key=} {idx=} ({init_func.__name__},{update.__name__})')
          init_func()


open_canvas()

ball = load_image('ball_41x41.png')
grass = load_image('grass.png')
reset()
update = reset

running = True
while running:
  clear_canvas()
  grass.draw(400, 30)
  ball.draw(x, y)
  update()

  update_canvas()
  handle_events()
  delay(0.01)
