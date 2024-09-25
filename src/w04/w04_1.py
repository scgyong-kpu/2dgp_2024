import gfw_loop
from grass import Grass

def enter():
  gfw_loop.game_objects.append(Grass())

gfw_loop.start(enter)


