from pico2d import * 
from gfw import *

world = World(['bg'])

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
    pass

def exit():
    world.clear()

def pause():
    print('[main.pause()]')

def resume():
    print('[main.resume()]')

def handle_event(e):
    if e.type == SDL_KEYDOWN and e.key == SDLK_1:
        print(world.objects)

    if e.type == SDL_KEYDOWN:
        if e.key == SDLK_LEFT:
            bg.x -= 10
        if e.key == SDLK_RIGHT:
            bg.x += 10

class ScrollBackground(Sprite):
    def __init__(self, filename):
        super().__init__(filename, 0, 0)

    def draw(self):
        self.image.draw_to_origin(self.x, self.y)

    def get_bb(self):
        return 0, 0, self.width, self.height

if __name__ == '__main__':
    gfw.start_main_module()

