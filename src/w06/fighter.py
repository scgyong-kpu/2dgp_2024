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

    def __init__(self):
        super().__init__('res/fighter.png', get_canvas_width() // 2, 80)
        self.dx = 0
        self.speed = 320 # 320 pixels per second
        half_width = self.image.w // 2
        self.min_x = half_width
        self.max_x = get_canvas_width() - half_width
        self.laser_time = 0
        self.spark_image = gfw.image.load('res/laser_0.png')
        self.roll_time = 0
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
        if self.dx == 0:
            self.roll_time = 0
        else:
            self.roll_time += self.dx * gfw.frame_time
            self.roll_time = clamp(-Fighter.MAX_ROLL, self.roll_time, Fighter.MAX_ROLL)
        print(f'roll={self.roll_time:.2f}')
    def draw(self):
        super().draw()
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
