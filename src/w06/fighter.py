from pico2d import *
import gfw

class Fighter(gfw.Sprite):
    def __init__(self):
        super().__init__('res/fighter.png', get_canvas_width() // 2, 80)

