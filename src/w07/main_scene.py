from pico2d import * 
from gfw import *
from boy import Boy

world = World(['bg', 'player'])

canvas_width = 1024
canvas_height = 768
# canvas_width = 1280
# canvas_height = 960
shows_bounding_box = True
shows_object_count = True

def enter():
    global bg
    bg = ScrollBackground('res/kpu_1280x960.png')
    world.append(bg, world.layer.bg)

    global boy
    boy = Boy()
    boy.bg = bg
    world.append(boy, world.layer.player)

def exit():
    world.clear()

def pause():
    print('[main.pause()]')

def resume():
    print('[main.resume()]')

def handle_event(e):
    if e.type == SDL_KEYDOWN and e.key == SDLK_1:
        print(world.objects)

    # if e.type == SDL_KEYDOWN:
    #     if e.key == SDLK_LEFT:
    #         bg.scroll(-10, 0)
    #     if e.key == SDLK_RIGHT:
    #         bg.scroll(10, 0)

    boy.handle_event(e)

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

    def get_bb(self):
        return 0, 0, self.width, self.height

if __name__ == '__main__':
    gfw.start_main_module()

