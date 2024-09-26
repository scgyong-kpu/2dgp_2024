from pico2d import *

running = True

stack = []

def start(scene):
    global current_scene
    current_scene = scene

    global stack
    stack = [scene]

    global running
    open_canvas() # canvas 를 열어서 화면을 준비한다

    current_scene.enter() # canvas 를 연 뒤에 해야 할 일이 있다면 하게 해 준다

    while running: # 무한루프를 돈다
        # update() 를 수행한다 (Game Logic)
        for go in current_scene.game_objects:
            go.update()

        # draw() 를 수행한다 (Rendering)
        clear_canvas()
        for go in current_scene.game_objects:
            go.draw()
        update_canvas()

        # event 를 처리한다
        for e in get_events():
            if e.type == SDL_QUIT:
                running = False
            else:
                current_scene.handle_event(e)

    current_scene.exit() # scene 종료 전에 할 일이 있으면 할 수 있는 기회를 준다

    close_canvas() # Game Loop 를 빠져 나왔으므로 화면을 닫는다

def start_main_module():
    import sys
    scene = sys.modules['__main__'] 
    # 시스템으로부터 __main__ 이라는 이름을 가진 module 객체를 얻어낸다

    start(scene)

def change(scene):
    global current_scene
    current_scene.exit()
    current_scene = scene
    print(f'{current_scene=}')
    current_scene.enter()

def push(scene):
    global current_scene
    stack.append(scene)
    current_scene = scene
    print(f'{current_scene=}')
    current_scene.enter()

def pop():
    global current_scene
    if len(stack) <= 1:
        running = False
        return

    current_scene.exit()
    stack.pop()
    current_scene = stack[-1]
    print(f'{current_scene=}')

