import gfw
from astar import AStarPath

SHORTENS = True
# SHORTENS = False

TILE_GRASS = 13

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
        self.path_coords = tiles

        # print(self.path_coords)
    def update(self): pass

    def draw(self):
        size = self.bg.tilesize
        for tx, ty in self.path_coords:
            x, y = map_bg.to_screen(tx, ty)
            self.image.draw(x, y, size, size)

def tile_to_coord(x, y=None):
    if y is None: 
        x, y = x
    return (x + 0.5) * map_bg.tilesize,  (y + 0.5) * map_bg.tilesize

def set_tile_bg(bg):
    global map_bg
    map_bg = bg

    search_install_positions()

    layer = bg.tmap.layers[1]

    ts = bg.tmap.tileheight
    mh = bg.tmap.height
    start_pos, end_pos = map(lambda o: (int(o['x'] // ts), mh - int(o['y'] // ts) - 1), layer.objects[0:2])

    global a_star
    a_star = MapPath(start_pos, end_pos, bg)

    global path_coords
    tiles = a_star.find_tiles()
    if not SHORTENS:
        path_coords = list(map(tile_to_coord, tiles))
        # print(f'{tiles=} {path_coords=}')
        return
    # print(f'{tiles=}')
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

def search_install_positions():
    global install_positions
    install_positions = []
    layer = map_bg.tmap.layers[0]
    for y in range(layer.height):
        for x in range(layer.width):
            tile = layer.data[y * layer.width + x]
            if tile == TILE_GRASS:
                install_positions.append(tile_to_coord(x, (layer.height - y - 1)))
    print(f'{len(install_positions)=}')

def can_install_at(x, y):
    print(f'{(x,y)=} {(x,y) in install_positions=} {len(install_positions)=} ')
    return (x, y) in install_positions

def spawn_pos():
    return path_coords[0]

def path_shower():
    return PathDraw(map_bg, install_positions)
