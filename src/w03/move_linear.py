from pico2d import *

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

def handle_events():
  global running, update
  for e in get_events():
    if e.type == SDL_QUIT:
      running = False
    elif e.type == SDL_KEYDOWN:
      if e.key == SDLK_ESCAPE:
        running = False
      elif e.key == SDLK_SPACE:
        global dx, dy
        dx, dy = 1.2, 0.7
        reset()
        update = update_delta


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
