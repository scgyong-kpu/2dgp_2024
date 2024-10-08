from pico2d import * 
import gfw

from fighter import Fighter
from enemy import EnemyGen

world = gfw.World(['bg', 'fighter', 'bullet', 'enemy', 'ui', 'controller'])

canvas_width = 500
canvas_height = 800
shows_bounding_box = True
shows_object_count = True

def enter():
    global fighter
    fighter = Fighter()
    world.append(fighter, world.layer.fighter)
    # world.append(MainScenUI(), world.layer.ui)
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
                        print(f'+{e.score} ={score}')
                        world.remove(e)
                    break
            if collided: break
            if gfw.collides_box(fighter, e):
                world.remove(e)
                # decrease fighter HP here?
                break

class MainScenUI:
    def __init__(self):
        self.font = load_font('res/lucon.ttf', 30)
        self.pos = (10, canvas_height - 20)
    def update(self): pass
    def draw(self):
        self.font.draw(*self.pos, str(list(map(len, world.objects))))

if __name__ == '__main__':
    gfw.start_main_module()

