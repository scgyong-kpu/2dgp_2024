import gfw
from ball import Ball

game_objects = []

def enter():
    game_objects.append(Ball())

def exit():
    game_objects.clear()
    print('[sub.exit()]')

def pause():
    pass

def resume():
    pass

def handle_event(e):
    pass

if __name__ == '__main__':
    gfw.start_main_module()

