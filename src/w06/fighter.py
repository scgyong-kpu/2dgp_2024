from pico2d import *
import gfw

class Fighter(gfw.Sprite):
    KEY_MAP = {
        (SDL_KEYDOWN, SDLK_LEFT):  -1,
        (SDL_KEYDOWN, SDLK_RIGHT):  1,
        (SDL_KEYUP, SDLK_LEFT):     1,
        (SDL_KEYUP, SDLK_RIGHT):   -1,
    }
    LASER_INTERVAL = 0.25
    SPARK_INTERVAL = 0.05
    SPARK_OFFSET = 28
    MAX_ROLL = 0.4
    IMAGE_RECTS = [
        (  8, 0, 42, 80),
        ( 76, 0, 42, 80),
        (140, 0, 50, 80),
        (205, 0, 56, 80),
        (270, 0, 62, 80),
        (334, 0, 70, 80),
        (406, 0, 62, 80),
        (477, 0, 56, 80),
        (549, 0, 48, 80),
        (621, 0, 42, 80),
        (689, 0, 42, 80),
    ]

    def __init__(self):
        super().__init__('res/fighters.png', get_canvas_width() // 2, 80)
        self.dx = 0
        self.speed = 320 # 320 pixels per second
        half_width = 36 # self.image.w // 2
        self.min_x = half_width
        self.max_x = get_canvas_width() - half_width
        self.laser_time = 0
        self.spark_image = gfw.image.load('res/laser_0.png')
        self.roll_time = 0
        self.src_rect = Fighter.IMAGE_RECTS[5] # 0~10 의 11 개 중 5번이 가운데이다.

    def handle_event(self, e):
        pair = (e.type, e.key)
        if pair in Fighter.KEY_MAP:
            self.dx += Fighter.KEY_MAP[pair]
    def update(self):
        self.x += self.dx * self.speed * gfw.frame_time
        self.x = clamp(self.min_x, self.x, self.max_x)
        self.laser_time += gfw.frame_time
        if self.laser_time >= Fighter.LASER_INTERVAL:
            self.fire()
        self.update_roll()
    def update_roll(self):
        roll_dir = self.dx
        if roll_dir == 0: # 현재 비행기가 움직이고 있지 않은데
            if self.roll_time > 0:   # roll 이 + 라면
                roll_dir = -1        #  감소시킨다
            elif self.roll_time < 0: # roll 이 - 라면
                roll_dir = 1         #  증가시킨다

        self.roll_time += roll_dir * gfw.frame_time
        self.roll_time = clamp(-Fighter.MAX_ROLL, self.roll_time, Fighter.MAX_ROLL)

        if self.dx == 0: # 현재 비행기가 움직이고 있지 않은데
            if roll_dir < 0 and self.roll_time < 0: # roll 이 감소중이었고 0 을 지나쳤으면
                self.roll_time = 0                  # 0 이 되게 한다
            if roll_dir > 0 and self.roll_time > 0: # roll 이 증가중이었고 0 을 지나쳤으면
                self.roll_time = 0                  # 0 이 되게 한다

        roll = int(self.roll_time * 5 / Fighter.MAX_ROLL)
        self.src_rect = Fighter.IMAGE_RECTS[roll + 5] # [-5 ~ +5] 를 [0 ~ 10] 으로 변환한다.
    def draw(self):
        # super().draw()
        self.image.clip_draw(*self.src_rect, self.x, self.y)
        if self.laser_time < Fighter.SPARK_INTERVAL:
            self.spark_image.draw(self.x, self.y + Fighter.SPARK_OFFSET)
    def fire(self):
        self.laser_time = 0
        world = gfw.top().world
        world.append(Bullet(self.x, self.y), world.layer.bullet)

class Bullet(gfw.Sprite):
    def __init__(self, x, y):
        super().__init__('res/laser_1.png', x, y)
        self.speed = 400 # 400 pixels per second
        self.max_y = get_canvas_height() + self.image.h
        self.layer_index = gfw.top().world.layer.bullet
    def update(self):
        self.y += self.speed * gfw.frame_time
        if self.y > self.max_y:
            gfw.top().world.remove(self)
