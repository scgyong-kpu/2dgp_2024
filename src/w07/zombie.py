import random
import time
import os
from pico2d import *
from gfw import *

class Node:
    BREAK, RETURN, RUNNING = range(3) # None for continue
    def add_child(self, child):
        self.children.append(child)
    def add_children(self, *children):
        for child in children:
            self.children.append(child)

class LeafNode(Node):
    def __init__(self, name, func):
        self.name = name
        self.func = func
    def run(self):
        return self.func()

class BehaviorTree(Node):
    def __init__(self, name, def_ret_val, children=[]):
        self.children = children
        self.name = name
        self.def_ret_val = def_ret_val
    def run(self):
        for pos in range(len(self.children)):
            # print(f'{pos}.{self.children[pos].name}')
            result = self.children[pos].run()
            if result == Node.RETURN:
                return Node.RETURN
            if result == Node.RUNNING:
                return Node.RUNNING
            if result == Node.BREAK:
                break
        return self.def_ret_val

class Zombie(AnimSprite):
    FPS = 12
    SCALE = 4
    GENDERS = ['male', 'female']
    IDLE_INTERVAL = 2.0
    DEAD_INTERVAL = 2.0
    def __init__(self):
        x, y = random.randrange(get_canvas_width()), random.randrange(get_canvas_height())
        super().__init__(None, x, y, self.FPS, 1)
        self.gender = random.choice(self.GENDERS)
        self.build_behavior_tree()
        self.set_action('Idle')
        self.load_images()
        self.width = self.images[0].w // self.SCALE
        self.height = self.images[0].h // self.SCALE
        self.flip = random.choice(['', 'h'])
        self.speed = random.uniform(50, 100)
        self.powerful = random.choice([True, False])
    def set_action(self, action):
        self.action = action
        print(f'{self.action=}')
        self.load_images()
        self.time = 0
    def load_images(self):
        self.images = load_image_series(f'res/zombiefiles/{self.gender}/{self.action} (%d).png')
        self.frame_count = len(self.images)
    def draw(self):
        main_scene = gfw.top()
        screen_pos = main_scene.bg.to_screen(self.x, self.y)
        index = round(self.time * self.fps)
        if self.action != 'Dead':
            index %= self.frame_count
        else:
            index = min(index, self.frame_count - 1)
        image = self.images[index]
        image.composite_draw(0, self.flip, *screen_pos, self.width, self.height)
    def update(self):
        self.time += gfw.frame_time
        self.bt.run()

    def do_idle(self):
        if self.action != 'Idle': 
            return None
        # print(f'{self.time}')
        if self.time < self.IDLE_INTERVAL:
            return None
        self.set_action('Walk')
        self.dx = 1 if self.flip == '' else -1
        self.dy = 0
        return Node.RETURN

    def do_walk(self):
        print(f'{self.action=} in do_walk()')
        if self.action != 'Walk':
            return None
        self.x += self.dx * self.speed * gfw.frame_time
        self.y += self.dy * self.speed * gfw.frame_time
        if (self.dx < 0 and self.x < 0) or (self.dx > 0 and self.x > get_canvas_width()):
            self.dx *= -1
            self.flip = '' if self.dx > 0 else 'h'
    def do_dead(self):
        if self.action != 'Dead': 
            return None
        if self.time > self.DEAD_INTERVAL:
            world = gfw.top().world
            world.remove(self, world.layer.zombie)
        return Node.RETURN
    def do_check_collision_with_player(self):
        player = gfw.top().boy
        collides = gfw.collides_box(player, self)
        if collides:
            self.set_action('Dead')
            return Node.RETURN
        return None
    CHASE_DISTANCE_SQ = 250 ** 2
    def do_find_player(self):
        player = gfw.top().boy
        dist_sq = distance_sq((player.x, player.y), (self.x, self.y))
        # print(f'{dist_sq=:.3f}')
        if dist_sq < self.CHASE_DISTANCE_SQ:
            if self.action != 'Attack':
                self.set_action('Attack')
            return None
        # print(f'{self.action=} in do_find_player()')
        if self.action == 'Attack':
            self.set_action('Idle')
            # self.dx, self.dy = 0, 0
        return Node.BREAK
    def move_to_target(self):
        self.x += self.dx * self.speed * gfw.frame_time
        self.y += self.dy * self.speed * gfw.frame_time
    def do_move_to_player(self):
        player = gfw.top().boy
        self.set_target(player.x, player.y)
        self.move_to_target()
        return Node.RETURN
    def do_patrol(self):
        # print('do_patrol')
        self.do_walk()
    def set_target(self, x, y):
        self.target = x, y
        dx, dy = x - self.x, y - self.y
        dist = math.sqrt(dx ** 2 + dy ** 2)
        if dist == 0:
            self.dx, self.dy = 0, 0
        else:
            self.dx, self.dy = dx / dist, dy / dist
        self.flip = '' if self.dx > 0 else 'h'

    def get_bb(self):
        half_width  = self.width * 9 // 20
        half_height = self.height * 9 // 20
        l = self.x - half_width
        b = self.y - half_height
        r = self.x + half_width
        t = self.y + half_width
        return l, b, r, t

    def build_behavior_tree(self):
        self.bt = BehaviorTree('Sequence', None, [
            LeafNode('Idle', self.do_idle),
            LeafNode('Dead', self.do_dead),
            BehaviorTree('Move', None, [
                BehaviorTree('FollowPlayer', None, [
                    LeafNode('CheckCollision', self.do_check_collision_with_player),
                    LeafNode('FindPlayer', self.do_find_player),
                    LeafNode('MoveToPlayer', self.do_move_to_player),
                ]),
                LeafNode('MoveToTarget', self.do_patrol),
            ])
        ])

def load_image_series(fmt):
    images = []
    index = 1
    while True:
        fn = fmt % index
        if not os.path.isfile(fn):
            break
        images.append(gfw.image.load(fn))
        index += 1
    # print(f'{fmt} {len(images)} images')
    return images

def distance_sq(point1, point2):
    x1,y1 = point1
    x2,y2 = point2
    return (x1-x2)**2 + (y1-y2)**2
