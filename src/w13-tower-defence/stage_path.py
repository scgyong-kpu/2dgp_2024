import gfw
from astar import AStarPath

# SHORTENS = True
SHORTENS = False

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

class PathDraw:
    def __init__(self, bg, tiles=[]):
        self.bg = bg
        self.image = gfw.image.load('res/trans_50b.png')
        self.path_tiles = tiles

        # print(self.path_tiles)
    def update(self): pass

    def draw(self):
        size = self.bg.tilesize
        for tx, ty in path_tiles:
            x, y = map_bg.to_screen(tx, ty)
            self.image.draw(x, y, size, size)

def set_tile_bg(bg):
    global map_bg
    map_bg = bg

    layer = bg.tmap.layers[1]

    ts = bg.tmap.tileheight
    mh = bg.tmap.height
    start_pos, end_pos = map(lambda o: (int(o['x'] // ts), mh - int(o['y'] // ts) - 1), layer.objects[0:2])

    global a_star
    a_star = MapPath(start_pos, end_pos, bg)

    def tile_to_coord(x, y=None):
        if y is None: 
            x, y = x
        return (x + 0.5) * map_bg.tilesize,  (y + 0.5) * map_bg.tilesize

    global path_tiles
    tiles = a_star.find_tiles()
    if not SHORTENS:
        path_tiles = list(map(tile_to_coord, tiles))
        # print(f'{tiles=} {path_tiles=}')
        return
    # print(f'{tiles=}')
    px,py = tiles.pop(0)
    path_tiles = [tile_to_coord(px,py)]
    while tiles:
        x,y = tiles.pop(0)
        if not tiles:
            path_tiles.append(tile_to_coord(x,y))
            break
        nx,ny = tiles[0]
        in_line = (x + x == px + nx and y + y == py + ny)
        px,py = x,y
        # print(f'{(px,py)=} {(x,y)=} {(nx,ny)=} {in_line=}')
        if not in_line:
            path_tiles.append(tile_to_coord(x,y))

    # print(f'{tiles=} {list(path_tiles)=}')

def path_shower():
    return PathDraw(map_bg, path_tiles)
