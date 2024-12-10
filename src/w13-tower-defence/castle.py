from pico2d import * 
from gfw import *
from cfg import cfg
import stage_path
from weapon import Explosion
import random

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

def hit(power):
    global life
    life -= power
    if life < 0: life = 0

def game_opver():
    return life <= 0

def update():
    world = gfw.top().world
    max_fire = 5 * (1 - life / max_life)
    cnt = world.count_at(world.layer.castle)
    if cnt < max_fire:
        hw, hh = castle_image.w/2, castle_image.h/2
        ex = x + random.randrange(hw) - hw/2
        ey = y + random.randrange(hh) - hh/2
        exp = Explosion('res/weapon/fireball_explosion.png', ex, ey, 15, 1)
        exp.layer_index = world.layer.castle
        world.append(exp)

def get_bb():
    return x - 70, y - 70, x + 70, y + 70
