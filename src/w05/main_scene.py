from pico2d import * 
import gfw
from boy import Boy

world = gfw.World(['bg', 'player', 'ball'])

def enter():
    cw, ch = get_canvas_width(), get_canvas_height()
    cx, cy = cw // 2, ch // 2
    world.append(gfw.Sprite('sky.jpg', cx, cy), world.layer.bg)
    world.append(gfw.Sprite('grass.png', cx, 30), world.layer.bg)
    world.append(gfw.Sprite('sun.png', cw - 100, ch - 100), world.layer.bg)
    world.append(gfw.AnimSprite('fireball.png', cx, cy, 8.3), world.layer.bg)
    world.append(gfw.AnimSprite('ryu.png', 200, 95, 9), world.layer.player)
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
        # gfw.push(sub_scene)
        return True # 이 이벤트는 처리했음을 알린다
    if e.type == SDL_KEYDOWN and e.key == SDLK_1:
        print(world.objects)

    boy.handle_event(e)

if __name__ == '__main__':
    gfw.start_main_module()

