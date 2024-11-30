import gfw
from astar import AStarPath

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
    def __init__(self):
        self.image = gfw.image.load('res/trans_50b.png')
    def update(self): pass

    def draw(self):
        size = map_bg.tilesize
        for tx, ty in path_tiles:
            x, y = map_bg.to_screen(tx * size, ty * size)
            self.image.draw_to_origin(x, y, size, size)

def set_tile_bg(bg):
    global map_bg
    map_bg = bg

    global a_star
    height = bg.tmap.height
    tuples = [ (int(o['x'] // 16), int(height - o['y'] // 16 - 1)) for o in bg.tmap.layers[1].objects]
    a_star = MapPath(*tuples, bg)

    global path_tiles
    path_tiles = a_star.find_tiles()

def path_shower():
    return PathDraw()

