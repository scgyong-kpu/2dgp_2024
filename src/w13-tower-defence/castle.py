from pico2d import * 
from gfw import *
from cfg import cfg
import stage_path

def init():
    global castle_image, x, y
    castle_image = gfw.image.load('res/castle.png')
    x, y = stage_path.castle_pos()
    y += 48

    global life, max_life
    max_life = cfg.stages[0].castle
    life = max_life

    global gauge
    gauge = Gauge('res/gauge_fg.png', 'res/gauge_bg.png')

def draw():
    castle_image.draw(x, y)
    gauge.draw(x, y - 74, castle_image.w - 20, life / max_life)

def update():
    global life
    life -= 0.1

def get_bb():
    return x - 70, y - 70, x + 70, y + 70
