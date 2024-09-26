from pico2d import *

images = {}

def load(file):
    global images
    if file in images:
        return images[file]

    image = load_image(file)
    images[file] = image
    return image

def unload(file):
    global images
    if file in images:
        del images[file]

class Sprite:
    def __init__(self, filename, x, y):
        self.filename = filename
        self.image = load(filename)
        self.x, self.y = x, y
    def draw(self):
        self.image.draw(self.x, self.y)
    def update(self):
        pass
