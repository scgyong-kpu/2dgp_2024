from pico2d import *
import gfw_image as image
from gfw_world import World

running = True

stack = []

def start(scene):
    open_canvas() # canvas 를 열어서 화면을 준비한다

    push(scene)

    while running: # 무한루프를 돈다
        # update() 를 수행한다 (Game Logic)
        for go in stack[-1].world.objects:
            go.update()

        # draw() 를 수행한다 (Rendering)
        clear_canvas()
        for go in stack[-1].world.objects:
            go.draw()
        update_canvas()

        # event 를 처리한다
        for e in get_events():
            handled = stack[-1].handle_event(e)
            if not handled:
                if e.type == SDL_QUIT:
                    quit()
                elif e.type == SDL_KEYDOWN:
                    if e.key == SDLK_ESCAPE:
                        pop()
                

    while stack:
        stack.pop().exit()
        # scene 종료 전에 할 일이 있으면 할 수 있는 기회를 준다

    close_canvas() # Game Loop 를 빠져 나왔으므로 화면을 닫는다

def start_main_module():
    import sys
    scene = sys.modules['__main__'] 
    # 시스템으로부터 __main__ 이라는 이름을 가진 module 객체를 얻어낸다

    start(scene)

def change(scene):
    if stack:
        stack.pop().exit()

    stack.append(scene)
    print(f'current_scene={scene}')
    scene.enter()

def push(scene):
    if stack:
        stack[-1].pause()

    stack.append(scene)
    print(f'current_scene={scene}')
    scene.enter()

def pop():
    stack.pop().exit()
    if not stack:
        quit()
        return

    scene = stack[-1]
    print(f'current_scene={scene}')
    scene.resume()

def quit():
    global running
    running = False

def top():
    return stack[-1]
