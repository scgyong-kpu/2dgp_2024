from pico2d import * 
import gfw

world = gfw.World(['bg'])

canvas_width = 1024
canvas_height = 768
shows_bounding_box = True
shows_object_count = True

def enter():
    pass

def exit():
    world.clear()

def pause():
    print('[main.pause()]')

def resume():
    print('[main.resume()]')

def handle_event(e):
    if e.type == SDL_KEYDOWN and e.key == SDLK_1:
        print(world.objects)


if __name__ == '__main__':
    gfw.start_main_module()

