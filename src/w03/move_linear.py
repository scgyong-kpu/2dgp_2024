from pico2d import *
import math

def char_draw():
  global frame_index
  character.clip_composite_draw(100 * frame_index, 0, 100, 100, 0, flip, x, y, 100, 100)
  frame_index = (frame_index + 1) % 8

def reset():
  global x, y
  x, y = 100, 100

def update_delta():
  global x, y
  x += dx
  y += dy
  # print(f'{x=} {y=} {dx=} {dy=}')

def update_angle():
  global x, y
  rad = math.radians(angle_degree)
  x += speed * math.cos(rad)
  y += speed * math.sin(rad)

def handle_events():
  global running, update
  for e in get_events():
    if e.type == SDL_QUIT:
      running = False
    elif e.type == SDL_KEYDOWN:
      if e.key == SDLK_ESCAPE:
        running = False
      elif e.key == SDLK_1:
        global dx, dy
        dx, dy = 1.2, 0.7
        reset()
        update = update_delta
      elif e.key == SDLK_2:
        global angle_degree, speed
        angle_degree = 19
        speed = 1.4
        reset()
        update = update_angle


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
