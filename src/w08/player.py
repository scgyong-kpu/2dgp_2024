from pico2d import * 
from gfw import *

class Cookie(Sprite):
    def __init__(self):
        super().__init__('res/cookie.png', 160, 160)
        self.running = True
        self.width, self.height = 138, 138
        self.src_rect = 69, 1090, 138, 138

    def handle_event(self, e):
        if e.type == SDL_KEYDOWN and e.key == SDLK_SPACE:
            self.toggle_state()

    def draw(self):
        self.image.clip_draw(*self.src_rect, self.x, self.y)

    def toggle_state(self):
        self.running = not self.running
        fn = 'res/cookie_run.png' if self.running else 'res/cookie_jump.png'
        self.image = load_image(fn)
        self.frame_count = self.image.w // self.image.h
