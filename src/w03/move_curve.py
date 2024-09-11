from pico2d import *
import math
import random

# pip install bezier 를 실행하여 설치해야 실행해 볼 수 있다.
import bezier

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

def jump_bounce():
  global x, y, dx, dy
  x += dx
  y += dy
  if dy < 0 and y <= BASE_Y: # 공이 아래로 떨어지고 있는 것을 확인해야 한다
    dy *= -0.8 # power가 여러 에너지로 변환되어 80% 만 남아있다.
    dx *= 0.8 # 앞으로 나아가는 힘도 줄었다
    if dy < 0.5: # 속도가 어느정도 이하가 되면 작은 숫자만큼 움직이는 것이 아니라 멈추는 것이 좋겠다
      dx, dy = 0, 0
      y = BASE_Y
  else:
    dy -= gravity

def parabola_init():
  global gravity, dx, dy
  dx = mouse_x * 0.5 * 0.01
  dy = mouse_y * 1.5 * 0.01
  gravity = 9.8 * 0.01

def circle_init():
  global cx, cy, radius, angle_radians, angle_speed
  cw, ch = get_canvas_width(), get_canvas_height()
  cx, cy = cw // 2, ch // 2
  radius = mouse_y - cy
  if radius < 0: radius *= -1
  if radius == 0: radius = 1
  angle_radians = 0
  angle_speed = (mouse_x - cx) * 0.05 * 0.01
  print(f'{cx=} {cy=} {radius=} {angle_speed=:.4f}')

def circle_update():
  global angle_radians, x, y
  angle_radians += angle_speed
  x = cx + radius * math.cos(angle_radians)
  y = cy + radius * math.sin(angle_radians)

def circle2_init():
  global cx, cy, radius, angle_radians, angle_speed
  cw, ch = get_canvas_width(), get_canvas_height()
  cx, cy = cw // 2, ch // 2
  radius = mouse_y - cy
  if radius < 0: radius *= -1
  if radius == 0: radius = 1
  angle_radians = 0
  speed = 2.4 # 등속 운동
  angle_speed = speed / radius #(mouse_x - cx) * 0.05 * 0.01
  print(f'{cx=} {cy=} {radius=} {angle_speed=:.4f}')

def bezier_init():
  global curves, curve_index, curve_count, progress
  nodes_array = [
    [[16.0, 88.5, 129.8, 129.8], [548.4, 541.2, 490.8, 428.9]],
    [[129.8, 129.8, 63.6, 64.4], [428.9, 367.0, 357.1, 290.2]],
    [[64.4, 65.1, 118.4, 186.7], [290.2, 223.4, 156.5, 155.8]],
    [[186.7, 254.9, 306.1, 307.6], [155.8, 155.1, 219.8, 288.8]],
    [[307.6, 309.0, 264.2, 264.9], [288.8, 357.8, 350.0, 422.5]],
    [[264.9, 265.6, 364.4, 402.1], [422.5, 495.0, 520.6, 520.6]],
    [[402.1, 439.8, 537.2, 538.0], [520.6, 520.6, 481.5, 425.3]],
    [[538.0, 538.7, 487.5, 487.5], [425.3, 369.2, 353.5, 291.6]],
    [[487.5, 487.5, 541.5, 616.9], [291.6, 229.8, 162.9, 163.6]],
    [[616.9, 692.3, 737.8, 735.6], [163.6, 164.4, 237.6, 294.5]],
    [[735.6, 733.5, 670.2, 670.9], [294.5, 351.4, 384.1, 442.4]],
    [[670.9, 671.6, 745.6, 791.1], [442.4, 500.7, 540.5, 537.0]],
  ]
  curves = [ bezier.Curve(nodes, degree=3) for nodes in nodes_array ]
  curve_index = 0
  curve_count = len(nodes_array)
  progress = 0

def bezier_update():
  global curve_index, progress, x, y
  progress += 0.01
  arr = curves[curve_index].evaluate(progress)
  x, y = arr[0][0], arr[1][0]
  if progress > 1: 
    progress = 0
    curve_index = (curve_index + 1) % curve_count

func_tables = [
  (reset, reset),
  (jump_init, jump_update),
  (parabola_init, jump_update),
  (parabola_init, jump_bounce),
  (circle_init, circle_update),
  (circle2_init, circle_update),
  (bezier_init, bezier_update),
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
