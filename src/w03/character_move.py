from pico2d import *

open_canvas()

grass = load_image('grass.png')
character = load_image('run_animation.png')

for x in range(0, 800):
  clear_canvas()
  grass.draw(400, 30)
  character.clip_draw(50, 50, 50, 50, x, 90)
  update_canvas()
  delay(0.01)

close_canvas()

