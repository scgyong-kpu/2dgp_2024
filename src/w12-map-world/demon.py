import math
import random
from pico2d import * 
from gfw import *
from map_helper import *

class Demon(AnimSprite):
    def __init__(self, type, x, y):
        fn, cnt, sp1, sp2 = INFO[type][1:5]
        super().__init__(fn, x, y, random.uniform(9, 11), cnt)
        self.layer_index = gfw.top().world.layer.enemy
        self.speed = random.uniform(sp1, sp2)
        self.info = INFO[type]
        self.flip = ''
        self.max_life = self.info[9]
        self.life = self.max_life
        self.gauge = Gauge('res/gauge_fg.png', 'res/gauge_bg.png')
        self.stun_timer = 0

    def check_stun(self):
        if self.stun_timer <= 0: return False
        self.stun_timer -= gfw.frame_time
        return True

    def hit(self, damage): #return True if dead
        if self.stun_timer > 0:
            return False
        self.life -= damage
        if self.life <= 0: return True
        self.stun_timer = 1.0
        return False

    def is_dead(self):
        return self.life <= 0

    def update(self):
        if self.check_stun():
            return
        world = gfw.top().world
        player = world.object_at(world.layer.player, 0)
        diff_x, diff_y = player.x - self.x, player.y - self.y
        dist = math.sqrt(diff_x ** 2 + diff_y ** 2)
        if dist >= 1:
            dx = self.speed * diff_x / dist * gfw.frame_time
            self.x += dx
            self.y += self.speed * diff_y / dist * gfw.frame_time
            self.flip = 'h' if dx > 0 else ''

    def draw(self):
        bg = gfw.top().world.bg
        index = self.get_anim_index()
        screen_pos = bg.to_screen(self.x, self.y)
        self.image.clip_composite_draw(index * self.width, 0, self.width, self.height, 0, self.flip, *screen_pos, self.width, self.height)
        gx, gy = screen_pos
        self.gauge.draw(gx, gy-20, self.width - 20, self.life / self.max_life)

    def get_bb(self):
        l, b, r, t = self.info[5:9]
        if self.flip == 'h':
            l,r = -r,-l
        return self.x+l, self.y+b, self.x+r, self.y+t

    def is_on_obstacle(self):
        return False

class LionDemon(Demon):
    def __init__(self, type, x, y):
        super().__init__(type, x, y)
        self.tx, self.ty = None, None

        world = gfw.top().world
        player = world.object_at(world.layer.player, 0)
        self.path_draw = PathDraw(player, world.bg)
        self.head_to_player()

    def head_to_player(self):
        world = gfw.top().world
        player = world.object_at(world.layer.player, 0)
        px = int(player.x // world.bg.tilesize)
        py = int(player.y // world.bg.tilesize)
        mx = int(self.x // world.bg.tilesize)
        my = int(self.y // world.bg.tilesize)
        a_star = MapPath((mx, my), (px, py), world.bg)
        a_star.off_border_wall = False
        tiles = a_star.find_tiles()
        if len(tiles) < 2:
            print(f'No path: {(mx, my)=}, {(px, py)=}')
            return
        x, y = tiles[1] # second tile
        self.tx, self.ty = (x + 0.5) * world.bg.tilesize, (y + 0.5) * world.bg.tilesize

        self.path_draw.set_tiles(tiles)

    def draw(self):
        self.path_draw.draw()
        super().draw()

    def update(self):
        if self.tx is None:
            print(f'{self.tx=}')
            return

        diff_x, diff_y = self.tx - self.x, self.ty - self.y
        dist = math.sqrt(diff_x ** 2 + diff_y ** 2)
        if dist < 1: 
            self.head_to_player() # find next tile
            return
        dx = self.speed * gfw.frame_time * diff_x / dist
        dy = self.speed * gfw.frame_time * diff_y / dist
        self.flip = 'h' if dx > 0 else ''
        self.x += dx
        self.y += dy

    def is_on_obstacle(self):
        world = gfw.top().world
        return world.bg.collides_box(*self.get_bb())

INFO = [
    (Demon, 'res/demon_itsumade.png', 0, 50, 100, -15, -15, 15, 15, 50),
    (Demon, 'res/demon_mizar.png', 12, 20, 50, -28, -5, 8, 31, 150),
    (LionDemon, 'res/demon_lion.png', 8, 40, 60, -25, -14, 25, 14, 100),
]

def position_somewhere_outside_screen():
    # MARGIN = -100
    MARGIN = 50
    bg = gfw.top().world.bg
    cw, ch = get_canvas_width(), get_canvas_height()
    l, b = bg.from_screen(0, 0)
    r, t = bg.from_screen(cw, ch)
    side = random.randint(1, 4)
    if side == 1: # left
        x, y = l - MARGIN, b + random.random() * ch
    elif side == 2: # bottom
        x, y = l + random.random() * cw, b - MARGIN
    elif side == 3: # right
        x, y = r + MARGIN, b + random.random() * ch
    else: # side == 4, up
        x, y = l + random.random() * cw, t + MARGIN
    # print(f'{side=} {(x,y)=}')
    return x, y

class DemonGen:
    def draw(self): pass
    def update(self):
        world = gfw.top().world
        if world.count_at(world.layer.enemy) >= 10: return
        type = random.randrange(len(INFO))
        # type = 2
        x, y = position_somewhere_outside_screen()
        clazz = INFO[type][0]
        demon = clazz(type, x, y)
        if demon.is_on_obstacle():
            return
        world.append(demon)