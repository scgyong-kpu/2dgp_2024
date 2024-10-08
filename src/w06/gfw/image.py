from pico2d import *

_images = {}

def load(file):
    global _images
    if file in _images:
        return _images[file]

    image = load_image(file)
    _images[file] = image
    return image

def unload(file):
    global _images
    if file in _images:
        del _images[file]

