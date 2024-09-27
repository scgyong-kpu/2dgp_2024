from pico2d import * 
import gfw

world = gfw.World(['bg'])

def enter():
    pass

def exit():
    world.clear()
    print('[main.exit()]')

def pause():
    print('[main.pause()]')

def resume():
    print('[main.resume()]')

def handle_event(e):
    if e.type == SDL_KEYDOWN and e.key == SDLK_1:
        print(world.objects)

if __name__ == '__main__':
    gfw.start_main_module()

