from pico2d import * 
from gfw import *
import random
import highscore_scene

world = World(['bg', 'card', 'ui'])

canvas_width = 960
canvas_height = 540
shows_bounding_box = False #True
shows_object_count = True

center_x = canvas_width // 2
center_y = canvas_height // 2

theme = {
    "title": "Enemy",
    "folder": "enemy"
}

def card_position(x, y):
    return (x + 1) * 120 - 30, (y + 1) * 120 - 28

class Card(AnimSprite):
    def __init__(self, x, y, folder, index):
        super().__init__(f'res/{folder}/back.png', *card_position(x, y), 10)
        self.folder = folder
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
            self.image = gfw.image.load(f'res/{self.folder}/f_{self.index:02d}.png')
        else:
            self.image = gfw.image.load(f'res/{self.folder}/back.png')
        self.width = self.image.h
        self.frame_count = self.image.w // self.image.h

class MainUi:
    def __init__(self):
        self.bg = gfw.image.load(f'res/round_rect_9.png')
        self.font = gfw.font.load(f'res/ENCR10B.TTF')
        self.nine = gfw.image.NinePatch(self.bg, 24, 24, 24, 24)
        self.score = 0
    def update(self): 
        if world.count_at(world.layer.card) > 0:
            self.score += gfw.frame_time
    def draw(self):
        self.nine.draw(790, center_y, 280, 460)
        self.font.draw(680, 450, ('Score: %5.1f' % self.score))


def enter():
    global folder
    folder = theme["folder"]
    world.append(Background(f'res/{folder}/bg.png'), world.layer.bg)
    indices = [ n for n in range(1, 11) ] * 2
    # print(f'Before: {indices=}')
    # random.shuffle(indices)
    # print(f'After : {indices=}')
    index = 0
    for y in range(4):
        for x in range(5):
            world.append(Card(x, y, folder, indices[index]), world.layer.card)
            index += 1
    global main_ui
    main_ui = MainUi()
    world.append(main_ui, world.layer.ui)

    global bg_music
    bg_music = gfw.sound.music(f'res/{folder}/bg.mp3')
    bg_music.set_volume(60)
    bg_music.repeat_play()

    global flip_wav
    flip_wav = gfw.sound.sfx(f'res/{folder}/flip.wav')

def exit():
    global bg_music
    del bg_music
    gfw.sound.unload(f'res/{folder}/bg.mp3')

    global flip_wav
    del flip_wav
    gfw.sound.unload(f'res/{folder}/flip.wav')

    world.clear()

def pause():
    print('[main.pause()]')
    bg_music.pause()

def resume():
    bg_music.resume()
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
    flip_wav.play()

    global shown_card
    if shown_card is not None:
        if card.index == shown_card.index:
            world.remove(card, world.layer.card)
            world.remove(shown_card, world.layer.card)
            shown_card = None
            main_ui.score -= 10
            if world.count_at(world.layer.card) == 0:
                bg_music.stop()
                highscore_scene.add(main_ui.score, theme['title'])
                gfw.push(highscore_scene)
            return
        shown_card.show(False)

    shown_card = card
    main_ui.score += 5

if __name__ == '__main__':
    gfw.start_main_module()

