from pico2d import *

_fonts = {}

def load(file, size=20):
    key = file + '_' + str(size)
    global _fonts
    if key in _fonts:
        return _fonts[key]

    # print("Loading font:", file, size)
    font = load_font(file, size)
    _fonts[key] = font
    return font

def unload(file, size=20):
    key = file + '_' + str(size)
    global _fonts
    if key in _fonts:
        del _fonts[key]
