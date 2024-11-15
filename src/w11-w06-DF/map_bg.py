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
        self.scroll_x, self.scroll_y = 150, 3220
    def update(self): 
        self.scroll_x += gfw.frame_time * 5
        self.scroll_y += gfw.frame_time * 20        
    def draw(self):
        for layer in self.tmap.layers:
            self.draw_layer(layer)
    def draw_layer(self, layer):
        cw,ch = get_canvas_width(), get_canvas_height()

        sx, sy = round(self.scroll_x), round(self.scroll_y)
        tile_x = sx // self.tilesize # 그려질 타일 크기 기준 어느 타일부터 시작할지
        tile_y = sy // self.tilesize

        beg_x = -(sx % self.tilesize);
        beg_y = -(sy % self.tilesize);


        dst_left, dst_top = beg_x, ch - beg_y
        ty = tile_y
        while dst_top > 0:
            tx = tile_x
            left = dst_left
            while left < cw:
                self.draw_tile(layer, tx, ty, left, dst_top)
                left += self.tilesize
                tx += 1
                if tx >= self.tmap.width: break
            dst_top -= self.tilesize
            ty += 1
            if ty >= self.tmap.height: break

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
        self.map_bg = MapBg('res/earth.json', 40)
        self.world.append(self.map_bg, 0)
    def exit(self): pass
    def handle_event(self, e): pass

if __name__ == '__main__':
    scene = TestScene()
    gfw.start(scene)


