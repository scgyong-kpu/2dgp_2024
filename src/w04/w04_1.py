from pico2d import * 
# SDL_*, SDLK_* 상수를 쓰려면 선언해야 한다

import gfw_loop
from grass import Grass
from boy import Boy

class MainScene:
    def enter(self):
        self.boy = Boy()
        gfw_loop.game_objects.append(self.boy)
        gfw_loop.game_objects.append(Grass())

    def handle_event(self, e):
        if e.type == SDL_KEYDOWN:
            if e.key == SDLK_LEFT:
                self.boy.x -= 10
            elif e.key == SDLK_RIGHT:
                self.boy.x += 10

scene = MainScene()

gfw_loop.start(scene)


