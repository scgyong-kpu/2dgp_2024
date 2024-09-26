from pico2d import * 
import gfw
from boy import Boy

world = gfw.World(['bg', 'player', 'ball'])

def enter():
    cx, cy = get_canvas_width() // 2, get_canvas_height() // 2
    world.append(gfw.Sprite('sky.jpg', cx, cy), world.layer.bg)
    global boy
    boy = Boy()
    world.append(boy, world.layer.player)

def exit():
    world.clear()
    print('[main.exit()]')

def pause():
    print('[main.pause()]')

def resume():
    print('[main.resume()]')

def handle_event(e):
    if e.type == SDL_KEYDOWN and e.key == SDLK_RETURN:
        gfw.push(sub_scene)
        return True # 이 이벤트는 처리했음을 알린다
    if e.type == SDL_KEYDOWN and e.key == SDLK_1:
        print(world.objects)

    boy.handle_event(e)

if __name__ == '__main__':
    gfw.start_main_module()

