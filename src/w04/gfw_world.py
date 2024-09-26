from pico2d import *
import gfw

class World:
    def __init__(self, layer_count=1):
        self.objects = [[]] * layer_count
        # self.objects = [[] for i in range(layer_count)]
    def append(self, go, layer_index=0):
        self.objects[layer_index].append(go)
    def remove(self, go, layer_index=0):
        self.objects[layer_index].remove(go)
    def clear(self):
        layer_count = len(self.objects)
        self.objects = [[]] * layer_count

    def all_objects(self):
        all_objs = []
        for objs in self.objects:
            all_objs += objs
        return all_objs
