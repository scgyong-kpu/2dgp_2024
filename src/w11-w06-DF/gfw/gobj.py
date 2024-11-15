import time
from pico2d import *
import gfw
from . import tiledmap

class Gauge:
    def __init__(self, fg_fname, bg_fname):
        self.fg = gfw.image.load(fg_fname)
        self.bg = gfw.image.load(bg_fname)
    def draw(self, x, y, width, rate):
        l = x - width // 2
        b = y - self.bg.h // 2
        self.draw_3(self.bg, l, b, width, 3)
        self.draw_3(self.fg, l, b, round(width * rate), 3)
    def draw_3(self, img, l, b, width, edge):
        img.clip_draw_to_origin(0, 0, edge, img.h, l, b, edge, img.h)
        img.clip_draw_to_origin(edge, 0, img.w - 2 * edge, img.h, l+edge, b, width - 2 * edge, img.h)
        img.clip_draw_to_origin(img.w - edge, 0, edge, img.h, l+width-edge, b, edge, img.h)

class Sprite:
    def __init__(self, filename, x, y):
        self.filename = filename
        if filename is None:
          self.image = None
          self.width, self.height = 0, 0
        else:
          self.image = gfw.image.load(filename)
          self.width, self.height = self.image.w, self.image.h
        self.x, self.y = x, y
    def draw(self):
        self.image.draw(self.x, self.y)
    def update(self):
        pass
    def get_bb(self):
        l = self.x - self.width // 2
        b = self.y - self.height // 2
        r = self.x + self.width // 2
        t = self.y + self.height // 2
        return l, b, r, t
    def contains_xy(self, x, y):
        l,b,r,t = self.get_bb()
        return l <= x < r and b <= y < t
    def __getstate__(self):
        dict = self.__dict__.copy()
        del dict['image']
        return dict
    def __setstate__(self, dict):
        self.__dict__.update(dict)
        # print(f'{self.filename=},')
        Sprite.__init__(self, self.filename, self.x, self.y)

    def __repr__(self):
        return f'{type(self).__name__}({self.filename})'

class AnimSprite(Sprite):
    def __init__(self, filename, x, y, fps, frame_count=0):
        super().__init__(filename, x, y)
        self.fps = fps
        if frame_count == 0: # 정사각형인 경우 0 을 주면 알아서 갯수를 세도록 한다
            frame_count = self.image.w // self.image.h

        if self.image is not None:
          self.width = self.image.w // frame_count
        self.frame_count = frame_count
        self.created_on = time.time()

    # elapsed time 을 구하기 위해 update() 에서 gfw.frame_time 을 누적하지 않는다
    # 그렇게 해도 되긴 하지만, 간단한 반복 애니메이션은 정확한 시간 누적이 필요한게 아니다
    # 오히려 AnimSprite 를 상속하는 객체가 super().update() 를 호출해야만 하는 부담이 생긴다

    def get_anim_index(self):
        elapsed = time.time() - self.created_on
        return round(elapsed * self.fps) % self.frame_count

    def draw(self):
        index = self.get_anim_index()
        self.image.clip_draw(index * self.width, 0, self.width, self.height, self.x, self.y)

class SheetSprite(AnimSprite):
    def __init__(self, fname, x, y, fps):
        super().__init__(fname, x, y, fps, 1)
        self.src_rects = []

    def draw(self):
        index = self.get_anim_index()
        src_rect = self.src_rects[index]
        self.image.clip_draw(*src_rect, self.x, self.y)

class ScoreSprite(Sprite):
    def __init__(self, img_file, right, y):
        super().__init__(img_file, right, y)
        self.digit_width = self.image.w // 10
        self.width = self.digit_width
        self.score = 0
        self.display = 0
    def draw(self):
        x = self.x
        score = self.display
        while score > 0:
            digit = score % 10
            sx = digit * self.digit_width
            # print(type(sx), type(digit), type(self.digit_width))
            self.image.clip_draw(sx, 0, self.digit_width, self.image.h, x, self.y)
            x -= self.digit_width
            score //= 10
    def update(self):
        diff = self.score - self.display;
        if diff == 0: return
        if -10 < diff and diff < 0:
            self.display -= 1
        elif 0 < diff and diff < 10:
            self.display += 1
        else:
            self.display += diff // 10

class Background(Sprite):
    def __init__(self, filename):
        cw, ch = get_canvas_width(), get_canvas_height()
        super().__init__(filename, cw // 2, ch // 2)
        self.width = cw
        self.height = ch

    def draw(self):
        self.image.draw(self.x, self.y, self.width, self.height)

class HorzFillBackground(Background):
    def __init__(self, filename, speed=0):
        super().__init__(filename)
        self.dest_width = self.image.w * get_canvas_height() // self.image.h
        self.speed = speed
        self.scroll = 0
    def update(self):
        self.scroll += self.speed * gfw.frame_time

    def draw(self):
        x = self.scroll % self.dest_width
        if x != 0: x -= self.dest_width
        max_x = get_canvas_width()
        while x < max_x:
            self.image.draw_to_origin(x, 0, self.dest_width, self.height)
            x += self.dest_width

class VertFillBackground(Background):
    def __init__(self, filename, speed=0):
        super().__init__(filename)
        self.dest_height = self.image.h * get_canvas_width() // self.image.w
        self.speed = speed
        self.scroll = 0
    def update(self):
        self.scroll += self.speed * gfw.frame_time

    def draw(self):
        y = self.scroll % self.dest_height
        if y != 0: y -= self.dest_height
        max_y = get_canvas_height()
        while y < max_y:
            self.image.draw_to_origin(0, y, self.width, self.dest_height)
            y += self.dest_height

class ScrollBackground(Sprite):
    def __init__(self, filename):
        super().__init__(filename, 0, 0)
        self.max_scroll_x = self.width - get_canvas_width()
        self.max_scroll_y = self.height - get_canvas_height()

    def draw(self):
        x, y = round(self.x), round(self.y)
        self.image.clip_draw_to_origin(x, y, get_canvas_width(), get_canvas_height(), 0, 0)

    def scroll(self, dx, dy):
        self.scrollTo(self.x + dx, self.y + dy)

    def scrollTo(self, x, y):
        self.x = clamp(0, x, self.max_scroll_x)
        self.y = clamp(0, y, self.max_scroll_y)

    def show(self, x, y):
        hw, hh = get_canvas_width() // 2, get_canvas_height() // 2
        self.x = clamp(0, x - hw, self.max_scroll_x)
        self.y = clamp(0, y - hh, self.max_scroll_y)

    def to_screen(self, x, y):
        return x - self.x, y - self.y

    def from_screen(self, x, y):
        return x + self.x, y + self.y

    def get_bb(self):
        return 0, 0, self.width, self.height

class InfiniteScrollBackground(ScrollBackground):
    def __init__(self, filename, margin=0):
        super().__init__(filename)
        self.margin = margin
    def scrollTo(self, x, y):
        self.x, self.y = x, y
    def show(self, x, y):
        cw, ch = get_canvas_width(), get_canvas_height()
        if self.margin > 0:
            if x < self.x + self.margin:
                self.x = x - self.margin
            elif x > self.x + cw - self.margin:
                self.x = x - cw + self.margin
            if y < self.y + self.margin:
                self.y = y - self.margin
            elif y > self.y + ch - self.margin:
                self.y = y - ch + self.margin
            return
        self.x = x - cw // 2
        self.y = y - ch // 2

    def draw(self):
        cw, ch = get_canvas_width(), get_canvas_height()

        # quadrant 3
        q3l = round(self.x) % self.width
        q3b = round(self.y) % self.height
        q3w = clamp(0, self.width - q3l, self.width)
        q3h = clamp(0, self.height - q3b, self.height)
        self.image.clip_draw_to_origin(q3l, q3b, q3w, q3h, 0, 0)

        # quadrant 2
        self.image.clip_draw_to_origin(q3l, 0, q3w, ch - q3h, 0, q3h)

        # quadrant 4
        self.image.clip_draw_to_origin(0, q3b, cw - q3w, q3h, q3w, 0)

        # quadrant 1
        self.image.clip_draw_to_origin(0, 0, cw - q3w, ch - q3h, q3w, q3h)

def _get_folder(filename):
    idx = filename.rfind('/')
    return '.' if idx < 0 else filename[:idx]

class MapBackground(InfiniteScrollBackground):
    def __init__(self, filename, tilesize=50, wraps=True, fitsWidth=False, fitsHeight=False, dx=0, dy=0):
        super().__init__(None)
        self.filename = filename
        self.folder = _get_folder(filename)
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
        self.layer = self.tmap.layers[0] # first layer only
        self.ts = self.tmap.tilesets[0] # first tileset only
        self.ts.rows = math.ceil(self.ts.tilecount / self.ts.columns) # 타일셋의 세로방향 타일 갯수를 구한다. 

    # TODO: show() 가 override 되어야 한다
    # def show(self, x, y):
    #     pass

    def set_scroll_speed(self, dx, dy):
        self.scroll_dx, self.scroll_dy = dx, dy
    def update(self): 
        self.x += gfw.frame_time * self.scroll_dx
        self.y += gfw.frame_time * self.scroll_dy
    def draw(self):
        layer = self.layer
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
                t_index = ty * layer.width + tx # 그 위치의 타일정보는 data[t_index] 에 있다
                tile = layer.data[t_index]   # 그려야 할 타일 번호를 구한다
                sx = (tile - 1) % self.ts.columns  # 해당 번호의 타일은 타일셋이미지 에서 왼쪽으로부터 sx 번째에 있다
                sy = (tile - 1) // self.ts.columns # 해당 번호의 타일은 타일셋이미지 에서 위로부터 sy 번째에 있다
                src_left = self.ts.margin + sx * (self.ts.tilewidth + self.ts.spacing) # 타일은 이미지의 src_left 번째 픽셀부터 시작 = 소스 x 좌표
                src_botm = self.ts.margin + (self.ts.rows - sy - 1) * (self.ts.tileheight + self.ts.spacing) # 소스 y 좌표.

                dst_botm = dst_top - self.tilesize
                self.ts.tile_image.clip_draw_to_origin(
                    src_left, src_botm, self.ts.tilewidth, self.ts.tileheight, 
                    left, dst_botm, self.tilesize, self.tilesize)

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

class Button(Sprite):
    def __init__(self, np_normal, np_over, font, title, x, y, width, height, on_click):
        super().__init__(None, x, y)
        self.bg_n = np_normal
        self.bg_o = np_over
        self.bg = np_normal
        self.width, self.height = width, height
        self.title = title
        self.font = font
        self._on_click = on_click

    def draw(self):
        self.bg.draw(self.x, self.y, self.width, self.height)
        gfw.font.draw_centered_text(self.font, self.title, self.x, self.y)

    def handle_event(self, e):
        if not self.contains_xy(*gfw.mouse_xy(e)): 
            self.bg = self.bg_n
            return False
        # print(e.type, self.title)
        if e.type == SDL_MOUSEBUTTONDOWN and e.button == SDL_BUTTON_LEFT:
            self._on_click()
        if e.type == SDL_MOUSEMOTION:
            self.bg = self.bg_o

