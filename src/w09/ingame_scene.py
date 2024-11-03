from pico2d import * 
from gfw import *

world = World(['bg', 'card', 'ui'])

canvas_width = 960
canvas_height = 540
shows_bounding_box = False #True
shows_object_count = True

center_x = canvas_width // 2
center_y = canvas_height // 2

def card_position(x, y):
    return (x + 1) * 120 - 30, (y + 1) * 120 - 28

class Card(AnimSprite):
    def __init__(self, x, y, index):
        super().__init__(f'res/back.png', *card_position(x, y), 10)
        self.index = index
        self.up = False

    def handle_mouse(self, x, y):
        if self.up: return 
        l, b, r, t = self.get_bb()
        if l <= x and x <= r and b <= y and y < t:
            self.show(True)
            return True
        return False

    def show(self, shows):
        self.up = shows
        if self.up:
            self.image = gfw.image.load(f'res/f_{self.index:02d}.png')
        else:
            self.image = gfw.image.load(f'res/back.png')
        self.width = self.image.h
        self.frame_count = self.image.w // self.image.h

class MainUi:
    def __init__(self):
        self.bg = gfw.image.load(f'res/round_rect_9.png')
        self.font = gfw.font.load(f'res/ENCR10B.TTF')
        self.nine = NinePatch(self.bg, 24, 24, 24, 24)
    def update(self): pass
    def draw(self):
        self.nine.draw(790, center_y, 280, 460)
        self.font.draw(680, 450, ('Score: %5.1f' % 123.4))

class NinePatch:
    def __init__(self, image, l, b, r, t):
        self.image = image
        self.margins = l, b, r, t

    def draw(self, x, y, width, height):
        self.draw_to_origin(x - width // 2, y - height // 2, width, height)

    def draw_to_origin(self, left, bottom, width, height):
        l, b, r, t = self.margins
        iw, ih = self.image.w, self.image.h
        dr, dt = left + width - r, bottom + height - t
        scw, sch = iw - l - r, ih - l - r
        dcw, dch = width - l - r, height - l - r
        self.image.clip_draw_to_origin(0, 0, l, b, left, bottom) # left-bottom
        self.image.clip_draw_to_origin(iw - r, 0, r, b, dr, bottom) # right-bottom
        self.image.clip_draw_to_origin(0, ih - t, l, t, left, dt) # left-top
        self.image.clip_draw_to_origin(iw - r, ih - t, r, t, dr, dt) # right-top
        self.image.clip_draw_to_origin(l, 0, scw, b, left + l, bottom, dcw, b) # center-bottom
        self.image.clip_draw_to_origin(0, b, l, sch, left, bottom + b, l, dch) # left-center
        self.image.clip_draw_to_origin(iw - r, b, r, sch, dr, bottom + b, r, dch) # right-center
        self.image.clip_draw_to_origin(l, ih-t, scw, t, left + l, dt, dcw, t) # center-top
        self.image.clip_draw_to_origin(l, b, scw, sch, left + l, bottom + b, dcw, dch) # center-center


def enter():
    world.append(Background('res/bg_andromeda.png'), world.layer.bg)
    index = 0
    for y in range(4):
        for x in range(5):
            world.append(Card(x, y, index // 2 + 1), world.layer.card)
            index += 1
    world.append(MainUi(), world.layer.ui)

def exit():
    world.clear()

def pause():
    print('[main.pause()]')

def resume():
    print('[main.resume()]')

def handle_event(e):
    if e.type == SDL_KEYDOWN and e.key == SDLK_1:
        print(world.objects)
        return

    if e.type == SDL_MOUSEBUTTONDOWN and e.button == SDL_BUTTON_LEFT:
        card_to_open = None
        for card in world.objects_at(world.layer.card):
            if card.handle_mouse(*gfw.mouse_xy(e)):
                card_to_open = card
                break
        if card_to_open is not None:
            open_card(card)

shown_card = None

def open_card(card):
    global shown_card
    if shown_card is not None:
        if card.index == shown_card.index:
            world.remove(card, world.layer.card)
            world.remove(shown_card, world.layer.card)
            shown_card = None
            return
        shown_card.show(False)

    shown_card = card

if __name__ == '__main__':
    gfw.start_main_module()

