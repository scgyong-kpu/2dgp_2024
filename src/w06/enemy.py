from pico2d import *
import gfw

class Enemy(gfw.AnimSprite):
    WIDTH = 100
    def __init__(self, index):
        x = self.WIDTH * index + self.WIDTH // 2
        y = get_canvas_height() + self.WIDTH // 2
        super().__init__('res/enemy_01.png', x, y, 10) # speed = 10fps
        self.speed = -100 # 100 pixels per second
        self.layer_index = gfw.top().world.layer.enemy
    def update(self):
        self.y += self.speed * gfw.frame_time
        if self.y < -self.WIDTH:
            gfw.top().world.remove(self)

class EnemyGen:
    GEN_INTERVAL = 5.0
    def __init__(self):
        self.time = 0
    def draw(self): pass
    def update(self):
        self.time += gfw.frame_time
        if self.time < self.GEN_INTERVAL:
            return
        gfw.top().world.append(Enemy(0))
        self.time -= self.GEN_INTERVAL

