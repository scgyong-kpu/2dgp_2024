from pico2d import *

open_canvas()

grass = load_image('grass.png')
character = load_image('run_animation.png')
frame_index = 0

for x in range(0, 800, 5):
  clear_canvas()
  grass.draw(400, 30)
  character.clip_draw(100 * frame_index, 0, 100, 100, x, 90, 200, 200)
  frame_index = (frame_index + 1) % 8
  update_canvas()
  delay(0.01)

close_canvas()

