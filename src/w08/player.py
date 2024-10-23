from pico2d import * 
from gfw import *

class Cookie(AnimSprite):
    def __init__(self):
        super().__init__('res/cookie_run.png', 160, 160, 10)
        self.running = True

    def handle_event(self, e):
        if e.type == SDL_KEYDOWN and e.key == SDLK_SPACE:
            self.toggle_state()

    def toggle_state(self):
        self.running = not self.running
        fn = 'res/cookie_run.png' if self.running else 'res/cookie_jump.png'
        self.image = load_image(fn)
        self.frame_count = self.image.w // self.image.h
