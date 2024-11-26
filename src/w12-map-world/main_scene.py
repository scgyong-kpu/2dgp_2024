from pico2d import * 
from gfw import *
from boy import Boy
from demon import Demon, DemonGen
from astar import AStarPath

world = gfw.World(['bg', 'enemy', 'item', 'player', 'ui', 'controller'])

canvas_width = 1280
canvas_height = 720
canvas_width = 1920
canvas_height = 1080
shows_bounding_box = True
shows_object_count = True

class CollisionChecker:
    def draw(self): pass
    def update(self):
        for obj in world.objects_at(world.layer.enemy):
            if collides_box(player, obj):
                world.remove(obj)
                break

class MapPath(AStarPath):
    def __init__(self, start_tuple, end_tuple, bg):
        super().__init__(start_tuple, end_tuple)
        self.bg = bg
    def is_wall(self, x, y):
        width, height = self.bg.layer.width, self.bg.layer.height
        if x < 0 or x >= width: return True
        if y < 0 or y >= height: return True
        tile = self.bg.layer.data[(height - y - 1) * width + x]
        return tile in self.bg.collision_tiles

class PathDraw:
    def __init__(self):
        self.image = gfw.image.load('res/trans_50b.png')
        self.a_star = MapPath((0,0),(0,0),world.bg)
        self.path_tiles = self.a_star.find_tiles()
        # self.path_tiles = [(0,0)]
        self.font = gfw.font.load('C:/Windows/Fonts/lucon.ttf', 13)
    def update(self): pass
    def draw(self):
        size = world.bg.tilesize
        for tx, ty in self.path_tiles:
            x, y = world.bg.to_screen(tx * size, ty * size)
            self.image.draw_to_origin(x, y, size, size)
        for (tx,ty),node in self.a_star.open_list.items():
            x, y = world.bg.to_screen(tx * size, ty * size)
            self.font.draw(x, y+10, f'{node}')
        for (tx,ty),node in self.a_star.close_list.items():
            x, y = world.bg.to_screen(tx * size, ty * size)
            self.font.draw(x, y+10, f'{node}', (0,0,127))
    def handle_event(self, e):
        px = int(player.x // world.bg.tilesize)
        py = int(player.y // world.bg.tilesize)
        mx, my = gfw.mouse_xy(e)
        mx, my = world.bg.from_screen(mx, my)
        mx = int(mx // world.bg.tilesize)
        my = int(my // world.bg.tilesize)

        self.a_star = MapPath( (px, py), (mx, my), world.bg)
        self.path_tiles = self.a_star.find_tiles()

        # layer = world.bg.layer
        # tile = layer.data[(layer.height - self.ty - 1) * layer.width + self.tx]
        # is_wall = tile in world.bg.collision_tiles
        # print(f'{self.tx=} {self.ty=} {tile=} {is_wall=}')

def enter():
    world.bg = MapBackground('res/desert.tmj', tilesize=100)
    world.bg.margin = 100
    world.bg.set_collision_tiles({1,2,3,9,10,11,17,18,19,20,21,25,26,27,28,29,33,34,35,36,37,41,42,43,44,45})
    world.append(world.bg, world.layer.bg)
    global player
    player = Boy()
    player.x *= 2
    player.y *= 2
    world.bg.x = player.x
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
    if e.type == SDL_MOUSEMOTION:
        path_draw.handle_event(e)
        return
    player.handle_event(e)

if __name__ == '__main__':
    gfw.start_main_module()

