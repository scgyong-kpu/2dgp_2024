import json
import math
import tiledmap
from gfw import *

def get_folder(filename):
    idx = filename.rfind('/')
    return '.' if idx < 0 else filename[:idx]

class MapBg:
    def __init__(self, filename, tilesize):
        self.map_filename = filename
        self.folder = get_folder(filename)
        self.tilesize = tilesize
        with open(filename, 'r') as f:
            mapjson = json.load(f)
        self.tmap = tiledmap.tiled_map_from_dict(mapjson)
        for ts in self.tmap.tilesets:
            ts.tile_image = gfw.image.load(f'{self.folder}/{ts.image}')
            # print(ts.tile_image)
    def update(self): pass
    def draw(self):
        for layer in self.tmap.layers:
            self.draw_layer(layer)
    def draw_layer(self, layer):
        tx, ty = 0, 0 # 0,0 위치의 타일을 그리겠다. map 의 0,0 은 좌상단이다.
        dst_left, dst_top = 0, get_canvas_height()
        self.draw_tile(layer, tx, ty, dst_left, dst_top)
    def draw_tile(self, layer, tx, ty, dst_left, dst_top):
        tileset = self.tmap.tilesets[0] # first tileset only
        rows = math.ceil(tileset.tilecount / tileset.columns) # 타일셋의 세로방향 타일 갯수를 구한다. 
        t_index = ty * layer.width + tx # 그 위치의 타일정보는 data[t_index] 에 있다
        tile = layer.data[t_index]   # 그려야 할 타일 번호를 구한다
        sx = (tile - 1) % tileset.columns  # 해당 번호의 타일은 타일셋이미지 에서 왼쪽으로부터 sx 번째에 있다
        sy = (tile - 1) // tileset.columns # 해당 번호의 타일은 타일셋이미지 에서 위로부터 sy 번째에 있다
        src_left = tileset.margin + sx * (tileset.tilewidth + tileset.spacing) # 타일은 이미지의 src_left 번째 픽셀부터 시작 = 소스 x 좌표
        src_botm = tileset.margin + (rows - sy - 1) * (tileset.tileheight + tileset.spacing) # 소스 y 좌표.

        dst_botm = dst_top - self.tilesize
        tileset.tile_image.clip_draw_to_origin(
            src_left, src_botm, tileset.tilewidth, tileset.tileheight, 
            dst_left, dst_botm, self.tilesize, self.tilesize)


class TestScene:
    def enter(self):
        self.world = World()
        self.map_bg = MapBg('res/earth.json', 100)
        self.world.append(self.map_bg, 0)
    def exit(self): pass
    def handle_event(self, e): pass

if __name__ == '__main__':
    scene = TestScene()
    gfw.start(scene)


