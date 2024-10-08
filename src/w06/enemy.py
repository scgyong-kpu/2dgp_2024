from pico2d import *
import random
import gfw

class Gauge:
    def __init__(self, fg_fname, bg_fname):
        self.fg = gfw.image.load(fg_fname)
        self.bg = gfw.image.load(bg_fname)
    def draw(self, x, y, width, rate):
        l = x - width // 2
        b = y - self.bg.h // 2
        self.draw_3(self.bg, l, b, width, 3)
        self.draw_3(self.fg, l, b, round(width * rate), 3)
    def draw_3(self, img, l, b, width, edge):
        img.clip_draw_to_origin(0, 0, edge, img.h, l, b, edge, img.h)
        img.clip_draw_to_origin(edge, 0, img.w - 2 * edge, img.h, l+edge, b, width - 2 * edge, img.h)
        img.clip_draw_to_origin(img.w - edge, 0, edge, img.h, l+width-edge, b, edge, img.h)

class Enemy(gfw.AnimSprite):
    WIDTH = 100
    MAX_LEVEL = 20
    gauge = None
    def __init__(self, index, level):
        x = self.WIDTH * index + self.WIDTH // 2
        y = get_canvas_height() + self.WIDTH // 2
        self.level = level
        # print(f'Creating Enemy Level {level}')
        super().__init__(f'res/enemy_{level:02d}.png', x, y, 10) # speed = 10fps
        self.speed = -100 # 100 pixels per second
        self.max_life = level * 100
        self.life = self.max_life
        if Enemy.gauge == None:
            Enemy.gauge = Gauge('res/gauge_fg.png', 'res/gauge_bg.png')
            print('Loading Gauge Only Once Here')
        self.layer_index = gfw.top().world.layer.enemy
    def update(self):
        self.y += self.speed * gfw.frame_time
        if self.y < -self.WIDTH:
            gfw.top().world.remove(self)
    def draw(self):
        super().draw()
        gy = self.y - self.WIDTH // 2
        rate = self.life / self.max_life
        self.gauge.draw(self.x, gy, self.WIDTH - 10, rate)
    def decrease_life(self, power):
        self.life -= power
        # print(f'Hit({power}/{self.life})')
        return self.life <= 0
    def get_bb(self):
        r = 42
        return self.x - r, self.y - r, self.x + r, self.y + r
    def __repr__(self):
        return f'Enemy({self.level}/{self.life})'

class EnemyGen:
    GEN_INTERVAL = 5.0
    GEN_INIT = 1.0
    GEN_X = [ 50, 150, 250, 350, 450 ]
    def __init__(self):
        self.time = self.GEN_INTERVAL - self.GEN_INIT
        self.wave_index = 0
    def draw(self): pass
    def update(self):
        self.time += gfw.frame_time * 5
        if self.time < self.GEN_INTERVAL:
            return
        for i in range(5):
            level = (self.wave_index + 18) // 10 - random.randrange(3)
            level = clamp(1, level, Enemy.MAX_LEVEL)
            gfw.top().world.append(Enemy(i, level))
        self.time -= self.GEN_INTERVAL
        self.wave_index += 1

