import random
import time
import os
from pico2d import *
from gfw import *

class Node:
    def add_child(self, child):
        self.children.append(child)
    def add_children(self, *children):
        for child in children:
            self.children.append(child)

class SelectorNode(Node):
    def __init__(self, name):
        self.children = []
        self.name = name
        self.prev_running_pos = 0
    def run(self):
        pass

class SequenceNode(Node):
    def __init__(self, name):
        self.children = []
        self.name = name
    def run(self):
        for pos in range(len(self.children)):
            result = self.children[pos].run()
            if result == BehaviorTree.SUCCESS:
                return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

class LeafNode(Node):
    def __init__(self, name, func):
        self.name = name
        self.func = func
    def run(self):
        return self.func()

class BehaviorTree:
    FAIL, RUNNING, SUCCESS = -1, 0, 1

    def __init__(self, root_node):
        self.root = root_node

    def run(self):
        self.root.run()


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
        self.speed = random.uniform(100, 150) * (1 if self.flip == '' else -1)
    def set_action(self, action):
        self.action = action
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
            index = min(index, self.frame_count)
        image = self.images[index]
        image.composite_draw(0, self.flip, *screen_pos, self.width, self.height)
    def update(self):
        self.time += gfw.frame_time
        self.bt.run()

    def do_idle(self):
        if self.action != 'Idle': 
            return BehaviorTree.FAIL
        if self.time < self.IDLE_INTERVAL:
            return BehaviorTree.SUCCESS
        self.set_action('Walk')
        return BehaviorTree.FAIL

    def do_walk(self):
        self.x += self.speed * gfw.frame_time
        if (self.speed < 0 and self.x < 0) or (self.speed > 0 and self.x > get_canvas_width()):
            self.speed *= -1
            self.flip = '' if self.speed > 0 else 'h'
        return BehaviorTree.SUCCESS
    def do_dead(self):
        if self.time > self.DEAD_INTERVAL:
            world = gfw.top().world
            world.remove(self, world.layer.zombie)

    def get_bb(self):
        half_width  = self.width * 9 // 20
        half_height = self.height * 9 // 20
        l = self.x - half_width
        b = self.y - half_height
        r = self.x + half_width
        t = self.y + half_width
        return l, b, r, t

    def build_behavior_tree(self):
        seq = SequenceNode('Sequence')
        seq.add_child(LeafNode('Idle', self.do_idle))
        seq.add_child(LeafNode('Walk', self.do_walk))
        self.bt = BehaviorTree(seq)

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
