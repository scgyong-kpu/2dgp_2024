from pico2d import *
import gfw

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
    if hasattr(a, 'get_bb'):
        la, ba, ra, ta = a.get_bb()
    else:
        la = a.x - a.width // 2
        ba = a.y - a.height // 2
        ra = a.x + a.width // 2
        ta = a.y + a.height // 2

    if hasattr(b, 'get_bb'):
        lb, bb, rb, tb = b.get_bb()
    else:
        lb = b.x - b.width // 2
        bb = b.y - b.height // 2
        rb = b.x + b.width // 2
        tb = b.y + b.height // 2

    if la > rb: return False
    if ra < lb: return False
    if ba > tb: return False
    if ta < bb: return False

    return True
