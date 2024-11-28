from pico2d import *
import random
import gfw

TWO_PI = math.pi * 2

class SoccerBall(gfw.Sprite):
    def __init__(self, player):
        super().__init__('res/ball21x21.png', 0, 0)
        self.player = player
        self.angle = 0
        self.radius = 100
        self.speed = 1 # one circle in 1 second
        self.power = 60

    def update(self):
        self.angle += self.speed * TWO_PI * gfw.frame_time
        if self.angle >= TWO_PI:
            self.angle -= TWO_PI
        self.x = self.player.x + self.radius * math.cos(self.angle)
        self.y = self.player.y + self.radius * math.sin(self.angle)
    def draw(self):
        bg = self.player.bg
        x, y = bg.to_screen(self.x, self.y)
        self.image.draw(x, y)

    def try_hit(self, obj): # returns False if obj is removed
        if gfw.collides_box(self, obj):
            if obj.hit(self.power):
                world = gfw.top().world
                world.remove(obj)
                return True
        return False

class Bomb(gfw.AnimSprite):
    def __init__(self, player):
        super().__init__('res/weapon_bomb.png', -100, -100, 10)
        self.player = player
        self.power = 80
        self.speed = 200
        self.angle = 0
        self.dx, self.dy = 0, 0
        self.reset()
    def reset(self):
        self.valid = False
    def fire(self):
        world = gfw.top().world
        if world.count_at(world.layer.enemy) == 0: return False
        demons = world.objects_at(world.layer.enemy)
        self.x, self.y = self.player.x, self.player.y
        INF = float('inf')
        nearest = min(demons, key=lambda d: INF if d.is_stunned() else (d.x - self.x) ** 2 + (d.y - self.y) ** 2)
        if nearest.is_stunned(): return False
        self.angle = math.atan2(nearest.y - self.y, nearest.x - self.x)
        self.dx = math.cos(self.angle) * self.speed
        self.dy = math.sin(self.angle) * self.speed
        self.valid = True
        return True
    def draw(self):
        bg = self.player.bg
        x, y = bg.to_screen(self.x, self.y)
        index = self.get_anim_index()
        self.image.clip_composite_draw(index * self.width, 0, self.width, self.height, self.angle, '', x, y, self.width, self.height)
    def update(self):
        self.x += self.dx * gfw.frame_time
        self.y += self.dy * gfw.frame_time

        l, b = self.player.bg.from_screen(0, 0)
        cw, ch = get_canvas_width(), get_canvas_height()
        r, t = self.player.bg.from_screen(cw, ch)
        if self.x < l or r < self.x or \
            self.y < b or t < self.y:
            self.reset()
    def try_hit(self, obj): # returns False if obj is removed
        if not gfw.collides_box(self, obj):
            return False
        if obj.is_stunned():
            return False

        dead = obj.hit(self.power)
        if dead:
            world = gfw.top().world
            world.remove(obj)
        self.reset()
        return dead
    def get_bb(self):
        r = 12 # radius
        return self.x-r, self.y-r, self.x+r, self.y+r

class Bombs:
    COOL_TIME = 1.0
    def __init__(self, player):
        self.player = player
        self.bombs = []
        self.time = self.COOL_TIME
        self.append()
        self.append()
    def append(self):
        bomb = Bomb(self.player)
        self.bombs.append(bomb)
    def update(self):
        fires = False
        if self.time > 0:
            self.time -= gfw.frame_time
        else:
            fires = True

        for b in self.bombs: 
            if b.valid: 
                b.update()
            elif fires:
                fires = False
                fired = b.fire()
                if fired:
                    self.time = self.COOL_TIME

    def draw(self):
        for b in self.bombs: 
            if b.valid: b.draw()
    def try_hit(self, obj):
        for b in self.bombs:
            if b.valid and b.try_hit(obj):
                return True
        return False

class Weapons:
    def __init__(self, player):
        self.weapons = []
    def append(self, weapon):
        self.weapons.append(weapon)
        if isinstance(weapon, SoccerBall):
            balls = [w for w in self.weapons if isinstance(w, SoccerBall)]
            count = len(balls)
            if count >= 2:
                step = TWO_PI / count
                angle = 0
                for ball in balls:
                    ball.angle = angle
                    angle += step
    def update(self):
        for w in self.weapons: w.update()
    def draw(self):
        for w in self.weapons: w.draw()
    def try_hit(self, obj):
        for w in self.weapons:
             if w.try_hit(obj):
                return True
        return False

class Boy(gfw.Sprite):
    def __init__(self):
        super().__init__('res/animation_sheet.png', get_canvas_width()//3, get_canvas_height()//2)
        self.time = 0 # age in seconds
        self.frame = 0
        self.dx, self.dy = 0, 0
        self.speed = 200
        self.action = 3 # 3=StandRight, 2=StandLeft, 1=RunRight, 0=RunLeft
        self.mag = 1
        self.target = None
        self.weapon = Bombs(self)
        # self.weapon = Weapons(self)
        # self.weapon.append(SoccerBall(self))
        # self.weapon.append(SoccerBall(self))
        # self.weapon.append(SoccerBall(self))
        # self.weapon.append(Bombs(self))

    # @property
    # def power(self):
    #     return self.weapon.power

    def draw(self):
        x = self.frame * 100
        y = self.action * 100
        screen_pos = self.bg.to_screen(self.x, self.y)
        self.image.clip_draw(x, y, 100, 100, *screen_pos)

    def update(self):

        self.time += gfw.frame_time
        fps, frame_count = 10, 8
        self.frame = round(self.time * fps) % frame_count
        dx = self.dx * self.speed * self.mag * gfw.frame_time
        dy = self.dy * self.speed * self.mag * gfw.frame_time
        l,b,r,t = self.get_bb()
        l,b,r,t = l+15,b+15,r-15,t-15
        if not self.bg.collides_box(l+dx,b,r+dx,t):
            self.x = clamp(self.bg.margin, self.x + dx, self.bg.total_width() - self.bg.margin)
        if not self.bg.collides_box(l,b+dy,r,t+dy):
            self.y = clamp(self.bg.margin, self.y + dy, self.bg.total_height() - self.bg.margin)
        if self.target is not None:
            tx, ty = self.target
            if (self.dx > 0 and self.x >= tx) or (self.dx < 0 and self.x <= tx):
                self.x, self.dx = tx, 0
            if (self.dy > 0 and self.y >= ty) or (self.dy < 0 and self.y <= ty):
                self.y, self.dy = ty, 0
            if self.dx == 0 and self.dy == 0:
                self.target = None
                self.adjust_action()
        self.bg.show(self.x, self.y)

    def adjust_delta(self, x, y):
        if self.target is not None:
            self.dx, self.dy = 0, 0
            self.target = None
        self.dx += x
        self.dy += y

    def set_target(self, mx, my):
        tx, ty = self.bg.from_screen(mx, my)
        if self.x == tx and self.y == ty:
            self.target = None
            self.dx, self.dy = 0, 0
            return
        self.target = tx, ty
        rad = math.atan2(ty - self.y, tx - self.x)
        self.dx, self.dy = math.cos(rad), math.sin(rad)

    def handle_event(self, e):
        dx, dy = self.dx, self.dy
        if e.type == SDL_KEYDOWN:
            if e.key == SDLK_LEFT:    self.adjust_delta(-1, 0)
            elif e.key == SDLK_RIGHT: self.adjust_delta(1, 0)
            elif e.key == SDLK_DOWN:  self.adjust_delta(0, -1)
            elif e.key == SDLK_UP:    self.adjust_delta(0, 1)
            elif e.key == SDLK_LSHIFT:
                self.mag *= 2

        elif e.type == SDL_KEYUP:
            if e.key == SDLK_LEFT:    self.adjust_delta(1, 0)
            elif e.key == SDLK_RIGHT: self.adjust_delta(-1, 0)
            elif e.key == SDLK_DOWN:  self.adjust_delta(0, 1)
            elif e.key == SDLK_UP:    self.adjust_delta(0, -1)
            elif e.key == SDLK_LSHIFT:
                self.mag //= 2

        elif e.type == SDL_MOUSEBUTTONDOWN:
            self.set_target(e.x, get_canvas_height() - e.y - 1)
        elif e.type == SDL_MOUSEMOTION:
            if self.target is not None:
                self.set_target(e.x, get_canvas_height() - e.y - 1)

        # print(f'({dx=}, {dy=}) != ({self.dx=}, {self.dy=})')
        if (dx, dy) != (self.dx, self.dy):
            self.adjust_action()

    def adjust_action(self):
            if self.dx > 0:
                self.action = 1
            elif self.dx < 0:
                self.action = 0
            else:
                if self.dy != 0: 
                    if self.action >= 2:
                        self.action -= 2
                else:
                    if self.action < 2:
                        self.action += 2

    def get_bb(self):
        hw, hh = 20, 34
        return self.x - hw, self.y - hh, self.x + hw, self.y + hh

    def __repr__(self):
        return 'Boy'
