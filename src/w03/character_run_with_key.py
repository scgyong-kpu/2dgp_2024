from pico2d import *

def handle_events():
  global running
  for e in get_events():
    if e.type == SDL_QUIT:
      running = False
    elif e.type == SDL_KEYDOWN:
      if e.key == SDLK_ESCAPE:
        running = False
      elif e.key == SDLK_LEFT:
        x -= 10
      elif e.key == SDLK_RIGHT:
        x += 10


open_canvas()

grass = load_image('grass.png')
character = load_image('run_animation.png')
frame_index = 0

x = 800 // 2
running = True

while running:
  clear_canvas()
  grass.draw(400, 30)
  character.clip_draw(100 * frame_index, 0, 100, 100, x, 90, 100, 100)
  frame_index = (frame_index + 1) % 8
  update_canvas()

  handle_events()

  delay(0.01)

close_canvas()

