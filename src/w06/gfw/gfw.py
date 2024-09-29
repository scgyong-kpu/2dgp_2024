from pico2d import *

import time

_running = True
_stack = []

def start(scene):
    import gfw

    w, h = 800, 600
    if hasattr(scene, 'canvas_width'): w = scene.canvas_width
    if hasattr(scene, 'canvas_height'): h = scene.canvas_height

    open_canvas(w=w, h=h, sync=True) # canvas 를 열어서 화면을 준비한다

    gfw.shows_bounding_box = scene.shows_bounding_box if hasattr(scene, 'shows_bounding_box') else False
    gfw.shows_object_count = scene.shows_object_count if hasattr(scene, 'shows_object_count') else False
    if gfw.shows_object_count: 
        _load_system_font()

    push(scene)

    global frame_time
    last_time = time.time()

    while _running: # 무한루프를 돈다

        # inter-frame (delta) time
        now = time.time()
        gfw.frame_time = now - last_time
        last_time = now

        # update() 를 수행한다 (Game Logic)
        _stack[-1].world.update()

        # draw() 를 수행한다 (Rendering)
        clear_canvas()
        _stack[-1].world.draw()
        update_canvas()

        # event 를 처리한다
        for e in get_events():
            handled = _stack[-1].handle_event(e)
            if not handled:
                if e.type == SDL_QUIT:
                    quit()
                elif e.type == SDL_KEYDOWN:
                    if e.key == SDLK_ESCAPE:
                        pop()

    while _stack:
        _stack.pop().exit()
        # scene 종료 전에 할 일이 있으면 할 수 있는 기회를 준다

    close_canvas() # Game Loop 를 빠져 나왔으므로 화면을 닫는다

def start_main_module():
    import sys
    scene = sys.modules['__main__'] 
    # 시스템으로부터 __main__ 이라는 이름을 가진 module 객체를 얻어낸다

    start(scene)

def change(scene):
    if _stack:
        _stack.pop().exit()

    _stack.append(scene)
    print(f'current_scene={scene}')
    scene.enter()

def push(scene):
    if _stack:
        _stack[-1].pause()

    _stack.append(scene)
    print(f'current_scene={scene}')
    scene.enter()

def pop():
    _stack.pop().exit()
    if not _stack:
        quit()
        return

    scene = _stack[-1]
    print(f'current_scene={scene}')
    scene.resume()

def quit():
    global _running
    _running = False

def top():
    return _stack[-1]

def _load_system_font():
    import gfw
    gfw._system_font = None
    paths = [ 'lucon.ttf', 'res/lucon.ttf', 'C:/Windows/Fonts/lucon.ttf' ]
    for path in paths:
        try:
            font = load_font(path, 20)
            print(f'System Font Loaded: {path}')
            gfw._system_font = font
            # print(f'{gfw.shows_object_count=} and {gfw._system_font=}')
            break
        except:
            pass
