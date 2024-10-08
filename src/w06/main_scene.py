from pico2d import * 
import gfw

from fighter import Fighter
from enemy import EnemyGen

world = gfw.World(['bg', 'fighter', 'bullet', 'enemy', 'ui', 'controller'])

canvas_width = 500
canvas_height = 800
shows_bounding_box = True
shows_object_count = True

class Background(gfw.Sprite):
    def __init__(self, filename):
        cw, ch = get_canvas_width(), get_canvas_height()
        super().__init__(filename, cw // 2, ch // 2)
        self.width = cw
        self.height = ch

    def draw(self):
        self.image.draw(self.x, self.y, self.width, self.height)

class VertFillBackground(Background):
    def __init__(self, filename, speed=0):
        super().__init__(filename)
        self.dest_height = self.image.h * get_canvas_width() // self.image.w
        self.speed = speed
        self.scroll = 0
    def update(self):
        self.scroll += self.speed * gfw.frame_time

    def draw(self):
        y = self.scroll % self.dest_height
        if y != 0: y -= self.dest_height
        max_y = get_canvas_height()
        while y < max_y:
            self.image.draw_to_origin(0, y, self.width, self.dest_height)
            y += self.dest_height

def enter():
    world.append(VertFillBackground('res/clouds.png', -60), world.layer.bg)
    world.append(VertFillBackground('res/bg_city.png', -30), world.layer.bg)
    global fighter
    fighter = Fighter()
    world.append(fighter, world.layer.fighter)
    # world.append(MainScenUI(), world.layer.ui)
    global score_sprite
    score_sprite = gfw.ScoreSprite('res/number_24x32.png', canvas_width - 50, canvas_height - 50)
    world.append(score_sprite, world.layer.ui)
    world.append(EnemyGen(), world.layer.controller)
    world.append(CollisionChecker(), world.layer.controller)


    global score
    score = 0

def exit():
    world.clear()
    print('[main.exit()]')

def pause():
    print('[main.pause()]')

def resume():
    print('[main.resume()]')

def handle_event(e):
    if e.type == SDL_KEYDOWN and e.key == SDLK_1:
        print(world.objects)
    fighter.handle_event(e)

class CollisionChecker:
    def draw(self): pass
    def update(self):
        enemies = world.objects_at(world.layer.enemy)
        for e in enemies: # reversed order
            collided = False
            bullets = world.objects_at(world.layer.bullet)
            for b in bullets: # reversed order
                if gfw.collides_box(b, e):
                    collided = True
                    world.remove(b)
                    dead = e.decrease_life(b.power)
                    if dead:
                        global score
                        score += e.score
                        score_sprite.score = score
                        # print(f'+{e.score} ={score}')
                        world.remove(e)
                    break
            if collided: break
            if gfw.collides_box(fighter, e):
                world.remove(e)
                # decrease fighter HP here?
                break

class MainScenUI:
    def __init__(self):
        self.font = load_font('res/lucon.ttf', 50)
        self.pos = (canvas_width - 320, canvas_height - 40)
    def update(self): pass
    def draw(self):
        self.font.draw(*self.pos, f'{score:10d}')


if __name__ == '__main__':
    gfw.start_main_module()

