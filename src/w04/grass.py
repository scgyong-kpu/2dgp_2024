from pico2d import *

def init():
    global image
    image = load_image('grass.png')

def draw():
    image.draw(400, 30)

def update():
    pass

