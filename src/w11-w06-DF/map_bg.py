import json
import math
import tiledmap
from gfw import *

def get_folder(filename):
    idx = filename.rfind('/')
    return '.' if idx < 0 else filename[:idx]

class MapBackground(InfiniteScrollBackground):
    def __init__(self, filename, tilesize=50, wraps=True, fitsWidth=False, fitsHeight=False, dx=0, dy=0):
        super().__init__(None)
        self.filename = filename
        self.folder = get_folder(filename)
        with open(filename, 'r') as f:
            mapjson = json.load(f)
        self.tmap = tiledmap.tiled_map_from_dict(mapjson)
        for ts in self.tmap.tilesets:
            ts.tile_image = gfw.image.load(f'{self.folder}/{ts.image}')
        if fitsWidth:
            tilesize = get_canvas_width() // self.tmap.width
        elif fitsHeight:
            tilesize = get_canvas_height() // self.tmap.height
        self.tilesize = tilesize
        self.wraps = wraps
        self.x, self.y = 0, 0
        self.scroll_dx, self.scroll_dy = dx, dy

    # TODO: show() 가 override 되어야 한다
    # def show(self, x, y):
    #     pass

    def set_scroll_speed(self, dx, dy):
        self.scroll_dx, self.scroll_dy = dx, dy
    def update(self): 
        self.x += gfw.frame_time * self.scroll_dx
        self.y += gfw.frame_time * self.scroll_dy
    def draw(self):
        for layer in self.tmap.layers:
            self.draw_layer(layer)
    def draw_layer(self, layer):
        cw,ch = get_canvas_width(), get_canvas_height()

        sx, sy = round(self.x), round(self.y)
        if self.wraps:
            map_total_width = self.tmap.width * self.tilesize
            map_total_height = self.tmap.height * self.tilesize
            sx %= map_total_width;
            if sx < 0:
                sx += map_total_width;
            sy %= map_total_height;
            if sy < 0:
                sy += map_total_width;

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
                if tx >= layer.width:
                    if not self.wraps: break
                    tx -= layer.width
            dst_top -= self.tilesize
            ty += 1
            if ty >= layer.height:
                if not self.wraps: break
                ty -= layer.height

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
        self.map_bg = MapBackground('res/earth.json', fitsWidth=True)
        self.world.append(self.map_bg, 0)
        # self.shows_bounding_box = True
    def exit(self): pass
    def handle_event(self, e):
        if e.type == SDL_KEYDOWN and e.key == SDLK_1:
            print(self.world.objects)
        if e.type == SDL_MOUSEMOTION:
            # dx = get_canvas_width() // 2 - e.x
            dx = 0
            dy = get_canvas_height() // 2 - e.y

            self.map_bg.set_scroll_speed(dx, dy)

if __name__ == '__main__':
    scene = TestScene()
    gfw.start(scene)


