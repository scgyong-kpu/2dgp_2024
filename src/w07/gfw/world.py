from pico2d import *
import gfw
from functools import reduce

class World:
    def __init__(self, layer_count=1):
        if isinstance(layer_count, list):
            layer_names = layer_count
            layer_count = len(layer_count)
            index = 0
            self.layer = lambda: None # 임의의 객체를 생성할 때 python 에서 즐겨 사용하는 방식
            for name in layer_names:
                self.layer.__dict__[name] = index
                index += 1

        self.objects = [[] for i in range(layer_count)]
    def append(self, go, layer_index=None):
        if layer_index is None:
            layer_index = go.layer_index
        self.objects[layer_index].append(go)
    def remove(self, go, layer_index=None):
        if layer_index is None:
            layer_index = go.layer_index
        self.objects[layer_index].remove(go)
    def clear(self):
        layer_count = len(self.objects)
        self.objects = [[] for i in range(layer_count)]
    def update(self):
        for go in self.all_objects():
            go.update()
    def draw(self):
        for go in self.all_objects():
            go.draw()
        if gfw.shows_bounding_box:
            for go in self.all_objects():
                if not hasattr(go, 'get_bb'): continue
                draw_rectangle(*go.get_bb())
        if gfw.shows_object_count and gfw._system_font is not None:
            gfw._system_font.draw(10, 20, str(list(map(len, self.objects))) + ' ' + str(self.count()))

    def all_objects(self):
        for objs in self.objects:
            for i in range(len(objs) - 1, -1, -1):
                yield objs[i]

    def objects_at(self, layer_index):
        objs = self.objects[layer_index]
        for i in range(len(objs) - 1, -1, -1):
            yield objs[i]

    def count_at(self, layer_index):
        return len(self.objects[layer_index])

    def count(self):
        return reduce(lambda sum, a: sum + len(a), self.objects, 0)

def collides_box(a, b): # a or b is a Sprite
    la, ba, ra, ta = a.get_bb()
    lb, bb, rb, tb = b.get_bb()

    if la > rb: return False
    if ra < lb: return False
    if ba > tb: return False
    if ta < bb: return False

    return True
