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

''' 다음 에러가 나타난다. World 의 외부에서 내부/구체적인 구현을 알고 있기 때문에 생기는 문제.
Pico2d is prepared.
current_scene=<module '__main__' from 'D://Lectures//2024_2//2dgp//git//src//w04//main_scene.py'>
Traceback (most recent call last):
  File "D:/Lectures/2024_2/2dgp/git/src/w04/main_scene.py", line 36, in <module>
    gfw.start_main_module()
  File "D:/Lectures/2024_2/2dgp/git/src/w04/gfw.py", line 47, in start_main_module
    start(scene)
  File "D:/Lectures/2024_2/2dgp/git/src/w04/gfw.py", line 17, in start
    go.update()
AttributeError: 'list' object has no attribute 'update'

'''
