from pico2d import *
import gfw

class Enemy(gfw.AnimSprite):
    WIDTH = 100
    def __init__(self, index, level):
        x = self.WIDTH * index + self.WIDTH // 2
        y = get_canvas_height() + self.WIDTH // 2
        self.level = level
        print(f'Creating Enemy Level {level}')
        super().__init__('res/enemy_01.png', x, y, 10) # speed = 10fps
        self.speed = -100 # 100 pixels per second
        self.layer_index = gfw.top().world.layer.enemy
    def update(self):
        self.y += self.speed * gfw.frame_time
        if self.y < -self.WIDTH:
            gfw.top().world.remove(self)
    def get_bb(self):
        r = 42
        return self.x - r, self.y - r, self.x + r, self.y + r
    def __repr__(self):
        return f'Enemy({self.level})'

class EnemyGen:
    GEN_INTERVAL = 5.0
    GEN_INIT = 1.0
    GEN_X = [ 50, 150, 250, 350, 450 ]
    def __init__(self):
        self.time = self.GEN_INTERVAL - self.GEN_INIT
        self.wave_index = 0
    def draw(self): pass
    def update(self):
        self.time += gfw.frame_time
        if self.time < self.GEN_INTERVAL:
            return
        for i in range(5):
            level = self.wave_index + i
            gfw.top().world.append(Enemy(i, level))
        self.time -= self.GEN_INTERVAL
        self.wave_index += 1

