from pico2d import *

def handle_events():
  global running
  global dx
  global x, y, flip

  for e in get_events():
    if e.type == SDL_QUIT:
      running = False
    elif e.type == SDL_KEYDOWN:
      if e.key == SDLK_ESCAPE:
        running = False
      elif e.key == SDLK_LEFT:
        dx -= 1
      elif e.key == SDLK_RIGHT:
        dx += 1
    elif e.type == SDL_KEYUP:
      if e.key == SDLK_ESCAPE:
        running = False
      elif e.key == SDLK_LEFT:
        dx += 1
      elif e.key == SDLK_RIGHT:
        dx -= 1
    elif e.type == SDL_MOUSEMOTION:
      mdx = e.x - x
      if mdx < 0: flip = 'h'
      if mdx > 0: flip = ''

      x, y = e.x, get_canvas_height() - e.y


open_canvas()

grass = load_image('grass.png')
character = load_image('run_animation.png')
frame_index = 0

x, y = get_canvas_width() // 2, get_canvas_height() // 2
dx = 0
running = True
flip = ''

while running:
  clear_canvas()
  grass.draw(400, 30)
  character.clip_composite_draw(100 * frame_index, 0, 100, 100, 0, flip, x, y, 100, 100)
  frame_index = (frame_index + 1) % 8
  x += dx
  if dx < 0: flip = 'h'
  if dx > 0: flip = ''
  print(f'{x=} {dx=:2} {flip=}')
  update_canvas()

  handle_events()

  delay(0.01)

close_canvas()

