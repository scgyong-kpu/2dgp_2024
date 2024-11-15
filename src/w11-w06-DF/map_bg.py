import json
import tiledmap
from gfw import *

def get_folder(filename):
    idx = filename.rfind('/')
    return '.' if idx < 0 else filename[:idx]

class MapBg:
    def __init__(self, filename):
        self.map_filename = filename
        self.folder = get_folder(filename)
        with open(filename, 'r') as f:
            mapjson = json.load(f)
        self.tmap = tiledmap.tiled_map_from_dict(mapjson)
        for ts in self.tmap.tilesets:
            ts.tile_image = gfw.image.load(f'{self.folder}/{ts.image}')
            print(ts.tile_image)

if __name__ == '__main__':
    open_canvas()
    mapbg = MapBg('res/earth.json')
    close_canvas()


