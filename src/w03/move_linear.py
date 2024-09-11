from pico2d import *
import math

def char_draw():
  global frame_index
  character.clip_composite_draw(100 * frame_index, 0, 100, 100, 0, flip, x, y, 100, 100)
  frame_index = (frame_index + 1) % 8

def set_direction():
  global flip
  if dx < 0: flip = 'h'
  if dx > 0: flip = ''

def reset():
  global x, y
  x, y = 100, 100

def init_delta():
  global dx, dy
  dx, dy = 1.2, 0.7
  set_direction()

def update_delta():
  global x, y
  x += dx
  y += dy
  # print(f'{x=} {y=} {dx=} {dy=}')

def init_angle():
  global dx, dy
  angle_radian = math.radians(19)
  speed = 1.4
  dx = speed * math.cos(angle_radian)
  dy = speed * math.sin(angle_radian)
  set_direction()

def init_mouse1():
  global dx, dy, tx, ty
  steps = 100
  dx = (mouse_x - x) / steps
  dy = (mouse_y - y) / steps
  tx, ty = mouse_x, mouse_y
  set_direction()

def init_mouse2():
  global dx, dy, tx, ty
  # x,y 는 reset() 이 불린 이후라 100,100 이다.
  angle_radian = math.atan2(mouse_y - y, mouse_x - x) 
  speed = 1.4
  dx = speed * math.cos(angle_radian)
  dy = speed * math.sin(angle_radian)
  tx, ty = mouse_x, mouse_y
  set_direction()

def update_to_target():
  global x, y, dx, dy
  x += dx
  if (dx > 0 and x > tx) or (dx < 0 and x < tx):
    x = tx
    dx = 0
  y += dy
  if (dy > 0 and y > ty) or (dy < 0 and y < ty):
    y = ty
    dy = 0

func_tables = [
  (reset, reset),
  (init_delta, update_delta),
  (init_angle, update_delta),
  (init_mouse1, update_to_target),
  (init_mouse2, update_to_target),
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

character = load_image('run_animation.png')
frame_index = 0
flip = ''
reset()
update = reset

running = True
while running:
  clear_canvas()
  char_draw()
  update()

  update_canvas()
  handle_events()
  delay(0.01)
