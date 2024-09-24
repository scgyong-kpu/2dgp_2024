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

gameObjects = [ grass ]
# for i in range(11):
# 	gameObjects.append(Boy())
boys = [ Boy() for i in range(11) ]
gameObjects += boys

print(len(gameObjects))

running = True
while running:
  clear_canvas()

  for gobj in gameObjects:
  	gobj.draw()

  update_canvas()

  for gobj in gameObjects:
  	gobj.update()

  handle_events()

  delay(0.05)

close_canvas()

