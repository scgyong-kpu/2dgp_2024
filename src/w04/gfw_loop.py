from pico2d import *

running = True

def start():
    global running
    open_canvas() # canvas 를 열어서 화면을 준비한다
    while running: # 무한루프를 돈다
        pass
        # update() 를 수행한다 (Game Logic)
        # draw() 를 수행한다 (Rendering)
        # event 를 처리한다
    close_canvas() # Game Loop 를 빠져 나왔으므로 화면을 닫는다

