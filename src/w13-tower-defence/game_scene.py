from pico2d import * 
from gfw import *

canvas_width = 1536 # 32 * 48
canvas_height = 864 # 18 * 48
shows_object_count = True

world = gfw.World(['bg', 'path'])


stage = 1
# stage = 2
# stage = 3

class PathDraw:
    def __init__(self, bg):
        self.bg = bg
        self.image = gfw.image.load('res/trans_50b.png')
        self.path_tiles = []

        print(self.path_tiles)
    def update(self): pass

    def draw(self):
        size = self.bg.tilesize
        for tx, ty in self.path_tiles:
            x, y = self.bg.to_screen(tx * size, ty * size)
            self.image.draw_to_origin(x, y, size, size)


def enter():
    global bg
    bg = MapBackground(f'res/map/stage_{stage:02d}.json', fitsHeight=True, wraps=False)
    layer = bg.tmap.layers[1]

    ts = bg.tmap.tileheight
    mh = bg.tmap.height
    start_pos, end_pos = map(lambda o: (int(o['x'] // ts), mh - int(o['y'] // ts) - 1), layer.objects[0:2])

    print(f'{start_pos=}, {end_pos=:}')

    pd = PathDraw(bg)
    pd.path_tiles = [ start_pos, end_pos ]
    world.append(bg, world.layer.bg)
    world.append(pd, world.layer.path)

def exit():
    world.clear()

# def pause():
#     print('[main.pause()]')

# def resume():
#     print('[main.resume()]')

def handle_event(e):
    if e.type == SDL_KEYDOWN and e.key == SDLK_1:
        print(world.objects)
        print(bg.tmap)
        return

if __name__ == '__main__':
    gfw.start_main_module()

