# class Grass:
# 	pass

# grass = Grass()
# print(grass)

from pico2d import *

def handle_events():
  global running
  global dx
  global tx, ty

  for e in get_events():
    if e.type == SDL_QUIT:
      running = False
    elif e.type == SDL_KEYDOWN:
      if e.key == SDLK_ESCAPE:
        running = False

open_canvas()

# import grass as grass_module
# grass = grass_module.Grass()

from grass import Grass
grass = Grass()

from boy import Boy
boy = Boy()

# load_image('grass.png')

gameObjects = [ boy, grass ]

running = True
while running:
  clear_canvas()

  for gobj in gameObjects:
  	gobj.draw()

  update_canvas()

  for gobj in gameObjects:
  	gobj.update()

  handle_events()

  delay(0.01)

close_canvas()

