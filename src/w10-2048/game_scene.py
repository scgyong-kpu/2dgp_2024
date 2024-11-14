import random
from pico2d import * 
from gfw import *
from board import Board
import highscore

world = World(['bg', 'block', 'over', 'ui'])

canvas_width = 520
canvas_height = 600
# shows_bounding_box = True
shows_object_count = True

class NumBlock(AnimSprite):
    SPEED_PPS = 3000
    MAG_SPEED = 0.15
    def __init__(self, n):
        fn = f'res/block_{n:05d}.png'
        super().__init__(fn, 0, 0, 10) # 10fps
        self.value = n
        self.being_born = True
        self.mag = 0
        self.layer_index = world.layer.block

    def double(self):
        self.value *= 2
        self.filename = f'res/block_{self.value:05d}.png'
        self.image = gfw.image.load(self.filename)

    def draw(self):
        index = self.get_anim_index()
        size = self.width * self.mag, self.height * self.mag
        self.image.clip_draw(index * self.width, 0, self.width, self.height, self.x, self.y, *size)

    def move_to(self, x, y, animates=True):
        tx = x * 120 + 80
        ty = y * 120 + 80
        if animates:
            self.tx, self.ty = tx, ty
        else:
            self.x, self.y = tx, ty
            self.tx, self.ty = None, None

    def update(self):
        if self.being_born:
            self.mag += (1.0/self.MAG_SPEED) * gfw.frame_time
            if self.mag >= 1.0:
                self.mag = 1.0
                self.being_born = False

        if self.tx is None: return
        dist = self.SPEED_PPS * gfw.frame_time
        x, y = self.x, self.y
        tx, ty = self.tx, self.ty
        if x < tx:
            x = min(x + dist, tx)
        elif x > tx:
            x = max(tx, x - dist)
        if y < ty:
            y = min(y + dist, ty)
        elif y > ty:
            y = max(ty, y - dist)

        self.x, self.y = x, y
        if (self.x, self.y) == (self.tx, self.ty):
            self.tx, self.ty = None, None

    def remove(self):
        world.remove(self)

    def __del__(self):
        print(f'Removing {self}')

def generate_block():
    if board.is_full(): return

    block = NumBlock(random.choice([2, 4]))
    x, y = board.generate_block(block)
    block.move_to(x, y, False)

    world.append(block)

def enter():
    highscore.load()

    world.append(Background('res/FF9F49.png'), world.layer.bg)

    global board
    board = Board()

    global score
    score = ScoreSprite('res/number_24x32.png', canvas_width - 30, canvas_height - 50)
    world.append(score, world.layer.ui)

    global game_over_sprite
    game_over_sprite = Background('res/game_over.png')

    start_game()

def start_game():
    world.clear_at(world.layer.over)
    board.clear()
    score.score = 0
    generate_block()

def end_game():
    board.slow_down()
    world.append(game_over_sprite, world.layer.over)
    world.append(highscore, world.layer.over)
    highscore.add(score.score)

def exit():
    global board, score, game_over_sprite
    board.clear()
    world.clear()

    del board, score, game_over_sprite

def pause():
    print('[main.pause()]')

def resume():
    print('[main.resume()]')

def handle_event(e):
    if e.type == SDL_KEYDOWN and e.key == SDLK_1:
        print(world.objects)
        return

    if e.type == SDL_KEYDOWN:
        moved, score_inc = False, 0
        if e.key == SDLK_LEFT:
            moved, score_inc = board.move_left()
        elif e.key == SDLK_RIGHT:
            moved, score_inc = board.move_right()
        elif e.key == SDLK_UP:
            moved, score_inc = board.move_up()
        elif e.key == SDLK_DOWN:
            moved, score_inc = board.move_down()
        elif e.key == SDLK_RETURN:
            if board.is_game_over():
                start_game()
        elif e.key == SDLK_BACKSPACE:
            board.clear()
        elif e.key == SDLK_2:
            num = 8
            while not board.is_full():
                block = NumBlock(num)
                x, y = board.generate_block(block)
                block.move_to(x, y, False)
                world.append(block)
                num = num * 2 if num < 10000 else 8
            if board.is_game_over():
                end_game()


        if score_inc != 0:
            score.score += score_inc
        if moved:
            generate_block()
            if board.is_game_over():
                end_game()

if __name__ == '__main__':
    gfw.start_main_module()

