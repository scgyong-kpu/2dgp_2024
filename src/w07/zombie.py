import random
import time
import os
from pico2d import *
from gfw import *
from behavior_tree import *

class Zombie(AnimSprite):
    FPS = 12
    SCALE = 4
    GENDERS = ['male', 'female']
    IDLE_INTERVAL = 2.0
    DEAD_INTERVAL = 2.0
    PAT_POSITIONS = [
        (43, 210), (1118, 210), (1050, 430), (575, 740), 
        (235, 927), (575, 740), (1050, 430), (1118, 210),
    ]
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
        self.patrol_index = -1
    def build_behavior_tree(self):
        self.bt = BehaviorTree(
            Selector('Root', [
                LeafNode('Idle', self.do_idle),
                LeafNode('Dead', self.do_dead),
                Sequence('FollowPlayer', [
                    LeafNode('CheckCollision', self.do_check_collision_with_player),
                    LeafNode('FindPlayer', self.do_find_player),
                    LeafNode('MoveToPlayer', self.do_move_to_player),
                ]),
                LeafNode('MoveToTarget', self.do_patrol),
            ])
        )

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
    def __getstate__(self):
        dict = super().__getstate__()
        del dict['images']
        del dict['bt']
        return dict

    def do_idle(self):
        if self.action != 'Idle': 
            return BT_FAIL
        # print(f'{self.time}')
        if self.time < self.IDLE_INTERVAL:
            return BT_SUCCESS
        self.set_action('Walk')
        self.patrol_index = -1
        return BT_SUCCESS

    def do_walk(self):
        # print(f'{self.action=} in do_walk()')
        if self.action != 'Walk':
            return BT_FAIL
        self.x += self.dx * self.speed * gfw.frame_time
        self.y += self.dy * self.speed * gfw.frame_time
        if (self.dx < 0 and self.x < 0) or (self.dx > 0 and self.x > get_canvas_width()):
            self.dx *= -1
            self.flip = '' if self.dx > 0 else 'h'
        return BT_SUCCESS

    def do_dead(self):
        if self.action != 'Dead': 
            return BT_FAIL
        if self.time > self.DEAD_INTERVAL:
            world = gfw.top().world
            world.remove(self, world.layer.zombie)
        return BT_SUCCESS
    def do_check_collision_with_player(self):
        player = gfw.top().boy
        collides = gfw.collides_box(player, self)
        if collides:
            self.set_action('Dead')
            return BT_FAIL # stop this sequence
        return BT_SUCCESS # continue
    CHASE_DISTANCE_SQ = 250 ** 2
    def do_find_player(self):
        player = gfw.top().boy
        dist_sq = distance_sq((player.x, player.y), (self.x, self.y))
        # print(f'{dist_sq=:.3f}')
        if dist_sq < self.CHASE_DISTANCE_SQ:
            if self.action != 'Attack':
                self.set_action('Attack')
            return BT_SUCCESS # continue
        # print(f'{self.action=} in do_find_player()')
        if self.action == 'Attack':
            self.set_action('Idle')
            # self.dx, self.dy = 0, 0
        return BT_FAIL # stop this sequence
    def move_to_target(self):
        self.x += self.dx * self.speed * gfw.frame_time
        self.y += self.dy * self.speed * gfw.frame_time
        tx, ty = self.target
        if (self.dx > 0 and self.x > tx) or\
            (self.dx < 0 and self.x < tx):
            self.x, self.dx = tx, 0
        if (self.dy > 0 and self.y > ty) or\
            (self.dy < 0 and self.y < ty):
            self.y, self.dy = ty, 0
        return self.dx == 0 and self.dy == 0
    def do_move_to_player(self):
        player = gfw.top().boy
        self.set_target(player.x, player.y)
        self.move_to_target()
        return BT_SUCCESS
    def do_patrol(self):
        if self.action != 'Walk':
            return BT_FAIL
        if self.patrol_index < 0:
            self.find_neareast_position()
            pos = self.PAT_POSITIONS[self.patrol_index]
            self.set_target(*pos)
        done = self.move_to_target()
        if done:
            self.patrol_index = (self.patrol_index + 1) % len(self.PAT_POSITIONS)
            pos = self.PAT_POSITIONS[self.patrol_index]
            print(f' patrol position #{self.patrol_index}: {pos}')
            self.set_target(*pos)
    def find_neareast_position(self):
        nearest = 0, float('inf')
        print(f'({self.x=:.2f}, {self.y=:.2f})')
        for i in range(len(self.PAT_POSITIONS)):
            px, py = self.PAT_POSITIONS[i]
            dsq = (self.x-px)**2 + (self.y-py)**2
            print(f' patrol position #{i}: {(px, py)}, {dsq=:.2f} dist={math.sqrt(dsq):.2f}')
            if nearest[1] > dsq:
                nearest = i, dsq

        print(f'nearest=#{nearest[0]}')
        self.patrol_index = nearest[0]
    def set_target(self, x, y):
        self.target = x, y
        dx, dy = x - self.x, y - self.y
        dist = math.sqrt(dx ** 2 + dy ** 2)
        if dist == 0:
            self.dx, self.dy = 0, 0
        else:
            self.dx, self.dy = dx / dist, dy / dist
        # print(f'{self.dx=}, {self.dy=}')
        self.flip = '' if self.dx > 0 else 'h'

    def get_bb(self):
        half_width  = self.width * 9 // 20
        half_height = self.height * 9 // 20
        l = self.x - half_width
        b = self.y - half_height
        r = self.x + half_width
        t = self.y + half_width
        return l, b, r, t

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
