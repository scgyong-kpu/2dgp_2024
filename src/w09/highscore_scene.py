from pico2d import * 
from gfw import *
import pickle

FILENAME = 'score.pickle'

world = World(2)

import sys
self = sys.modules[__name__]

class Entry:
    def __init__(self, score):
        self.score = score
        self.time = time.localtime()
    def timestr(self):
        return time.strftime('%Y-%m-%d %H:%M:%S', self.time)


try:
    f = open(FILENAME, "rb")
    scores = pickle.load(f)
    f.close()
    print("Scores:", scores)
except:
    print("No highscore file")
    scores = [ Entry(score) for score in range(100, 200, 10) ]

def enter():
    global frame_9p
    frame_9p = gfw.image.NinePatch(gfw.image.load('res/hs_frame.png'), 30, 30, 30, 30)
    global font
    font = gfw.font.load('res/ENCR10B.TTF', 25)
    world.append(self, 1)

def exit():
    world.clear()

def update():
    pass

def draw():
    cw, ch = get_canvas_width(), get_canvas_height()
    frame_9p.draw(cw // 2, ch // 2, cw - 100, ch - 100)
    x, y = 150, ch - 120
    for score in scores:
        font.draw(x, y, f'{score.score:5d}')
        font.draw(x + 200, y, score.timestr())
        y -= 40

def pause():
    print('[main.pause()]')

def resume():
    print('[main.resume()]')

def handle_event(e):
    if e.type == SDL_KEYDOWN and e.key == SDLK_1:
        print(world.objects)
        return

if __name__ == '__main__':
    gfw.start_main_module()

