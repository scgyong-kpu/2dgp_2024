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
            for go in objs:
                yield go 
        # generator 를 사용하면 all_objs 같이 메모리를 할당하지 않아도 된다

    def objects_at(self, layer_index):
        for go in self.objects[layer_index]:
            yield go 
