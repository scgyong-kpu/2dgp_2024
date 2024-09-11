from pico2d import *
import math
import random

BASE_Y = 65

def reset():
  global x, y
  x, y = 100, BASE_Y

def jump_init():
  global power, gravity, dx, dy
  power, gravity = 900 * 0.01, 9.8 * 0.01
  dx, dy = 0, power

def jump_update():
  global x, y, dx, dy
  x += dx
  y += dy
  if y <= BASE_Y:
    dx,dy = 0,0
    y = BASE_Y
  else:
    dy -= gravity

def parabola_init():
  global gravity, dx, dy
  dx = mouse_x * 0.5 * 0.01
  dy = mouse_y * 1.5 * 0.01
  gravity = 9.8 * 0.01

func_tables = [
  (reset, reset),
  (jump_init, jump_update),
  (parabola_init, jump_update),
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
