from astar import AStarPath
from gfw import *

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
        return tile in self.bg.collision_tiles

class PathDraw:
    def __init__(self, player, bg):
        self.image = gfw.image.load('res/trans_50b.png')
        self.a_star = MapPath((0,0),(0,0),bg)
        self.path_tiles = self.a_star.find_tiles()
        self.player = player
        self.bg = bg
        # self.path_tiles = [(0,0)]
    def update(self): pass

    def draw(self):
        size = self.bg.tilesize
        for tx, ty in self.path_tiles:
            x, y = self.bg.to_screen(tx * size, ty * size)
            self.image.draw_to_origin(x, y, size, size)
    def handle_event(self, e):
        px = int(self.player.x // self.bg.tilesize)
        py = int(self.player.y // self.bg.tilesize)
        mx, my = gfw.mouse_xy(e)
        mx, my = self.bg.from_screen(mx, my)
        mx = int(mx // self.bg.tilesize)
        my = int(my // self.bg.tilesize)

        self.a_star = MapPath( (px, py), (mx, my), self.bg)
        self.path_tiles = self.a_star.find_tiles()

