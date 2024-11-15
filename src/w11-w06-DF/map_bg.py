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
    def update(self): pass
    def draw(self):
        pass

class TestScene:
    def enter(self):
        self.world = World()
        self.map_bg = MapBg('res/earth.json')
        self.world.append(self.map_bg, 0)
    def exit(self): pass
    def handle_event(self, e): pass

if __name__ == '__main__':
    scene = TestScene()
    gfw.start(scene)


