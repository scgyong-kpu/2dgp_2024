import gfw
from ball import Ball

world = gfw.World()

def enter():
    world.append(Ball())

def exit():
    world.clear()
    print('[sub.exit()]')

def pause():
    pass

def resume():
    pass

def handle_event(e):
    pass

if __name__ == '__main__':
    gfw.start_main_module()

