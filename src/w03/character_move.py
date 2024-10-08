from pico2d import *

open_canvas()

grass = load_image('grass.png')
character = load_image('run_animation.png')
frame_index = 0

rad = 0
flip = ''

for x in range(0, 800):
  clear_canvas()
  grass.draw(400, 30)
  # flip = 'h' if x // 200 % 2 == 0 else ''
  # flip += 'v' if (x - 100) // 200 % 2 == 0 else ''
  rad += math.pi / 100
  # pi/100 만큼 더하고 있어서 x 가 100 증가할때마다 반바퀴씩 돈다.
  print(f'{x=:3d}, {flip=}, {rad=:5.2f}')
  character.clip_composite_draw(100 * frame_index, 0, 100, 100, rad, flip, x, 90, 200, 200)
  frame_index = (frame_index + 1) % 8
  update_canvas()
  delay(0.01)

close_canvas()

