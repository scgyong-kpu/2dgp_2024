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

    def draw(self):
        self.image.draw_to_origin(-self.x, -self.y)

    def scroll(self, dx, dy):
        self.scrollTo(self.x + dx, self.y + dy)

    def scrollTo(self, x, y):
        self.x = clamp(0, x, self.width - get_canvas_width())
        self.y = clamp(0, y, self.height - get_canvas_height())

    def get_bb(self):
        return 0, 0, self.width, self.height

if __name__ == '__main__':
    gfw.start_main_module()

