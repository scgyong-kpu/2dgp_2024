from pico2d import *
import gfw

class World:
    def __init__(self):
        self.objects = []
    def append(self, go):
        self.objects.append(go)
    def remove(self, go):
        self.objects.remove(go)
    def clear(self):
        self.objects = []
