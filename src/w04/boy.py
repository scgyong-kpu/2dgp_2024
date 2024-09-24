from pico2d import *

class Boy:
    def __init__(self):
        self.image = load_image('character.png')
    def draw(self):
        self.image.draw(400, 90)

