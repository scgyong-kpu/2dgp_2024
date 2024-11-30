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
        for tx, ty in path_coords:
            x, y = map_bg.to_screen(tx, ty)
            self.image.draw(x, y, size, size)

def set_tile_bg(bg):
    global map_bg
    map_bg = bg

    global a_star
    height = bg.tmap.height
    tuples = [ (int(o['x'] // 16), int(height - o['y'] // 16 - 1)) for o in bg.tmap.layers[1].objects]
    a_star = MapPath(*tuples, bg)

    def tile_to_coord(x, y):
        return (x + 0.5) * map_bg.tilesize,  (y + 0.5) * map_bg.tilesize

    global path_coords
    tiles = a_star.find_tiles()
    print(f'{tiles=}')
    px,py = tiles.pop(0)
    path_coords = [tile_to_coord(px,py)]
    while tiles:
        x,y = tiles.pop(0)
        if not tiles:
            path_coords.append(tile_to_coord(x,y))
            break
        nx,ny = tiles[0]
        in_line = (x + x == px + nx and y + y == py + ny)
        px,py = x,y
        # print(f'{(px,py)=} {(x,y)=} {(nx,ny)=} {in_line=}')
        if not in_line:
            path_coords.append(tile_to_coord(x,y))
    print(f'{path_coords=}')

def spawn_pos():
    return path_coords[0]


def path_shower():
    return PathDraw()

