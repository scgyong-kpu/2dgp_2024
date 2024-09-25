from pico2d import *

game_objects = []
running = True

def start(enter_function):
    global running
    open_canvas() # canvas 를 열어서 화면을 준비한다

    enter_function() # canvas 를 연 뒤에 해야 할 일이 있다면 하게 해 준다

    while running: # 무한루프를 돈다
        # update() 를 수행한다 (Game Logic)
        for go in game_objects:
            go.update()

        # draw() 를 수행한다 (Rendering)
        clear_canvas()
        for go in game_objects:
            go.draw()
        update_canvas()

        # event 를 처리한다
        for e in get_events():
            if e.type == SDL_QUIT:
                running = False

    close_canvas() # Game Loop 를 빠져 나왔으므로 화면을 닫는다

