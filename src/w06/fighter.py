from pico2d import *
import gfw

class Fighter(gfw.Sprite):
    KEY_MAP = {
        (SDL_KEYDOWN, SDLK_LEFT):  -1,
        (SDL_KEYDOWN, SDLK_RIGHT):  1,
        (SDL_KEYUP, SDLK_LEFT):     1,
        (SDL_KEYUP, SDLK_RIGHT):   -1,
    }
    def __init__(self):
        super().__init__('res/fighter.png', get_canvas_width() // 2, 80)
        self.dx = 0
        self.speed = 320 # 320 pixels per second
    def handle_event(self, e):
        pair = (e.type, e.key)
        if pair in Fighter.KEY_MAP:
            self.dx += Fighter.KEY_MAP[pair]
    def update(self):
        self.x += self.dx * self.speed * gfw.frame_time
        self.x = clamp(0, self.x, get_canvas_width())


