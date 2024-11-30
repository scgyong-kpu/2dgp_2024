from pico2d import * 
from gfw import *
from astar import *

canvas_width = 1536 # 32 * 48
canvas_height = 864 # 18 * 48
shows_object_count = True

world = gfw.World(['bg', 'path'])

class MapPath(AStarPath):
    def __init__(self, start_tuple, end_tuple, bg):
        super().__init__(start_tuple, end_tuple)
        self.bg = bg
        self.off_border_wall = True
    def is_wall(self, x, y):
        width, height = self.bg.layer.width, self.bg.layer.height
        if x < 0 or x >= width: return self.off_border_wall
        if y < 0 or y >= height: return self.off_border_wall
        tile = self.bg.layer.data[(height - y - 1) * width + x]
        return tile != 11
        # return tile in self.bg.collision_tiles

class PathDraw:
    def __init__(self, bg):
        self.bg = bg
        self.image = gfw.image.load('res/trans_50b.png')
        height = bg.tmap.height
        tuples = [ (int(o['x'] // 16), int(height - o['y'] // 16 - 1)) for o in bg.tmap.layers[1].objects]
        print(tuples)
        self.a_star = MapPath( *tuples, self.bg)
        self.path_tiles = self.a_star.find_tiles()

        print(self.path_tiles)
    def update(self): pass

    def draw(self):
        size = self.bg.tilesize
        for tx, ty in self.path_tiles:
            x, y = self.bg.to_screen(tx * size, ty * size)
            self.image.draw_to_origin(x, y, size, size)

stage = 1

def enter():
    global bg
    json_fn = f'res/map/stage_{stage:02d}.json'
    bg = MapBackground(json_fn, fitsHeight=True, wraps=False)

    world.append(bg, world.layer.bg)
    world.bg = bg

    global map_path
    map_path = PathDraw(bg)

    world.append(map_path, world.layer.path)

def exit():
    world.clear()

# def pause():
#     print('[main.pause()]')

# def resume():
#     print('[main.resume()]')

def handle_event(e):
    if e.type == SDL_KEYDOWN and e.key == SDLK_1:
        print(world.objects)
        print(bg.tmap)
        return

if __name__ == '__main__':
    gfw.start_main_module()

