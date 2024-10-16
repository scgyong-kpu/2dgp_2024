import gfw
from pico2d import *
import main_scene

import sys
self = sys.modules[__name__]

canvas_width = main_scene.canvas_width
canvas_height = main_scene.canvas_height

center_x = canvas_width // 2
center_y = canvas_height // 2

world = gfw.World(2)

def enter():
    self.gauge = gfw.Gauge('res/progress_bg.png', 'res/progress_fg.png')
    self.font = load_font('res/ENCR10B.TTF', 30)

    world.append(gfw.Sprite('res/loading_1280x960.png', center_x, center_y), 0)
    world.append(self, 1)

    self.image_index = 0
    self.image_count = len(IMAGE_FILES)
    self.images = iter(IMAGE_FILES)
    self.file = ''
    self.progress_y = canvas_height // 3
    self.progress_w = canvas_width * 2 // 3
    self.other_x = center_x - self.progress_w // 2
    self.color = (87, 41, 138) #57298a
    # print(len(list(images)))

def update():
    self.file = next(images, None)
    if file is None:
        gfw.change(main_scene)
        return
    print(f'Loading {file=}')
    gfw.image.load(file)
    self.image_index += 1

def draw():
    progress = image_index / image_count
    gauge.draw(center_x, progress_y, progress_w, progress)
    font.draw(other_x, progress_y - 50, self.file, self.color)
    font.draw(other_x, progress_y + 50, '%.1f%%' % (progress * 100), self.color)

def exit():
    gfw.image.unload('res/loading_1280x960.png')
    gfw.image.unload('res/progress_bg.png')
    gfw.image.unload('res/progress_fg.png')
    world.clear()
    del self.font

def handle_event(e):
    pass

IMAGE_FILES = [
    "res/kpu_1280x960.png",
    "res/animation_sheet.png",
    "res/zombiefiles/female/Attack (1).png",
    "res/zombiefiles/female/Attack (2).png",
    "res/zombiefiles/female/Attack (3).png",
    "res/zombiefiles/female/Attack (4).png",
    "res/zombiefiles/female/Attack (5).png",
    "res/zombiefiles/female/Attack (6).png",
    "res/zombiefiles/female/Attack (7).png",
    "res/zombiefiles/female/Attack (8).png",
    "res/zombiefiles/female/Attack (9).png",
    "res/zombiefiles/female/Attack (10).png",
    "res/zombiefiles/female/Dead (1).png",
    "res/zombiefiles/female/Dead (2).png",
    "res/zombiefiles/female/Dead (3).png",
    "res/zombiefiles/female/Dead (4).png",
    "res/zombiefiles/female/Dead (5).png",
    "res/zombiefiles/female/Dead (6).png",
    "res/zombiefiles/female/Dead (7).png",
    "res/zombiefiles/female/Dead (8).png",
    "res/zombiefiles/female/Dead (9).png",
    "res/zombiefiles/female/Dead (10).png",
    "res/zombiefiles/female/Dead (11).png",
    "res/zombiefiles/female/Dead (12).png",
    "res/zombiefiles/female/Idle (1).png",
    "res/zombiefiles/female/Idle (2).png",
    "res/zombiefiles/female/Idle (3).png",
    "res/zombiefiles/female/Idle (4).png",
    "res/zombiefiles/female/Idle (5).png",
    "res/zombiefiles/female/Idle (6).png",
    "res/zombiefiles/female/Idle (7).png",
    "res/zombiefiles/female/Idle (8).png",
    "res/zombiefiles/female/Idle (9).png",
    "res/zombiefiles/female/Idle (10).png",
    "res/zombiefiles/female/Idle (11).png",
    "res/zombiefiles/female/Idle (12).png",
    "res/zombiefiles/female/Idle (13).png",
    "res/zombiefiles/female/Idle (14).png",
    "res/zombiefiles/female/Idle (15).png",
    "res/zombiefiles/female/Walk (1).png",
    "res/zombiefiles/female/Walk (2).png",
    "res/zombiefiles/female/Walk (3).png",
    "res/zombiefiles/female/Walk (4).png",
    "res/zombiefiles/female/Walk (5).png",
    "res/zombiefiles/female/Walk (6).png",
    "res/zombiefiles/female/Walk (7).png",
    "res/zombiefiles/female/Walk (8).png",
    "res/zombiefiles/female/Walk (9).png",
    "res/zombiefiles/female/Walk (10).png",
    "res/zombiefiles/male/Attack (1).png",
    "res/zombiefiles/male/Attack (2).png",
    "res/zombiefiles/male/Attack (3).png",
    "res/zombiefiles/male/Attack (4).png",
    "res/zombiefiles/male/Attack (5).png",
    "res/zombiefiles/male/Attack (6).png",
    "res/zombiefiles/male/Attack (7).png",
    "res/zombiefiles/male/Attack (8).png",
    "res/zombiefiles/male/Dead (1).png",
    "res/zombiefiles/male/Dead (2).png",
    "res/zombiefiles/male/Dead (3).png",
    "res/zombiefiles/male/Dead (4).png",
    "res/zombiefiles/male/Dead (5).png",
    "res/zombiefiles/male/Dead (6).png",
    "res/zombiefiles/male/Dead (7).png",
    "res/zombiefiles/male/Dead (8).png",
    "res/zombiefiles/male/Dead (9).png",
    "res/zombiefiles/male/Dead (10).png",
    "res/zombiefiles/male/Dead (11).png",
    "res/zombiefiles/male/Dead (12).png",
    "res/zombiefiles/male/Idle (1).png",
    "res/zombiefiles/male/Idle (2).png",
    "res/zombiefiles/male/Idle (3).png",
    "res/zombiefiles/male/Idle (4).png",
    "res/zombiefiles/male/Idle (5).png",
    "res/zombiefiles/male/Idle (6).png",
    "res/zombiefiles/male/Idle (7).png",
    "res/zombiefiles/male/Idle (8).png",
    "res/zombiefiles/male/Idle (9).png",
    "res/zombiefiles/male/Idle (10).png",
    "res/zombiefiles/male/Idle (11).png",
    "res/zombiefiles/male/Idle (12).png",
    "res/zombiefiles/male/Idle (13).png",
    "res/zombiefiles/male/Idle (14).png",
    "res/zombiefiles/male/Idle (15).png",
    "res/zombiefiles/male/Walk (1).png",
    "res/zombiefiles/male/Walk (2).png",
    "res/zombiefiles/male/Walk (3).png",
    "res/zombiefiles/male/Walk (4).png",
    "res/zombiefiles/male/Walk (5).png",
    "res/zombiefiles/male/Walk (6).png",
    "res/zombiefiles/male/Walk (7).png",
    "res/zombiefiles/male/Walk (8).png",
    "res/zombiefiles/male/Walk (9).png",
    "res/zombiefiles/male/Walk (10).png",
]

if __name__ == '__main__':
    gfw.start_main_module()
