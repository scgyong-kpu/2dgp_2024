from pico2d import * 
from gfw import *
from boy import Boy
from demon import Demon, DemonGen

world = gfw.World(['bg', 'enemy', 'item', 'player', 'ui', 'controller'])

canvas_width = 1280
canvas_height = 720
shows_bounding_box = True
shows_object_count = True

class CollisionChecker:
    def draw(self): pass
    def update(self):
        for obj in world.objects_at(world.layer.enemy):
            if collides_box(player, obj):
                world.remove(obj)
                break

class PathDraw:
    def __init__(self):
        self.image = gfw.image.load('res/trans_50b.png')
    def update(self): pass
    def draw(self):
        self.image.draw(400, 400, 100, 100)

def enter():
    world.bg = MapBackground('res/desert.tmj', tilesize=30)
    world.bg.margin = 100
    world.bg.set_collision_tiles({1,2,3,9,10,11,17,18,19,20,21,25,26,27,28,29,33,34,35,36,37,41,42,43,44,45})
    world.append(world.bg, world.layer.bg)
    global player
    player = Boy()
    player.bg = world.bg
    world.append(player, world.layer.player)

    global path_draw
    path_draw = PathDraw()
    world.append(path_draw, world.layer.ui)

    world.append(DemonGen(), world.layer.controller)
    world.append(CollisionChecker(), world.layer.controller)

def exit():
    world.clear()

def pause():
    print('[main.pause()]')

def resume():
    print('[main.resume()]')

def handle_event(e):
    if e.type == SDL_KEYDOWN and e.key == SDLK_1:
        print(world.objects)
        return
    player.handle_event(e)

if __name__ == '__main__':
    gfw.start_main_module()

