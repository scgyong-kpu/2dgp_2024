from pico2d import *
import gfw

class World:
    def __init__(self, layer_count=1):
        self.objects = [[] for i in range(layer_count)]
    def append(self, go, layer_index=0):
        self.objects[layer_index].append(go)
    def remove(self, go, layer_index=0):
        self.objects[layer_index].remove(go)
    def clear(self):
        layer_count = len(self.objects)
        self.objects = [[]] * layer_count
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
