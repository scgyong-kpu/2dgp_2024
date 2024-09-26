from pico2d import *
import time

_images = {}

def load(file):
    global _images
    if file in _images:
        return _images[file]

    image = load_image(file)
    _images[file] = image
    return image

def unload(file):
    global _images
    if file in _images:
        del _images[file]

class Sprite:
    def __init__(self, filename, x, y):
        self.filename = filename
        self.image = load(filename)
        self.x, self.y = x, y
        self.width, self.height = self.image.w, self.image.h
    def draw(self):
        self.image.draw(self.x, self.y)
    def update(self):
        pass
    def __repr__(self):
        return f'{type(self).__name__}({self.filename})'

class AnimSprite(Sprite):
    def __init__(self, filename, x, y, fps, frame_count=0):
        super().__init__(filename, x, y)
        self.fps = fps
        if frame_count == 0: # 정사각형인 경우 0 을 주면 알아서 갯수를 세도록 한다
            frame_count = self.image.w // self.image.h

        self.width = self.image.w // frame_count
        self.frame_count = frame_count
        self.created_on = time.time()

    # elapsed time 을 구하기 위해 update() 에서 gfw.frame_time 을 누적하지 않는다
    # 그렇게 해도 되긴 하지만, 간단한 반복 애니메이션은 정확한 시간 누적이 필요한게 아니다
    # 오히려 AnimSprite 를 상속하는 객체가 super().update() 를 호출해야만 하는 부담이 생긴다
    def draw(self):
        elpased = time.time() - self.created_on
        index = round(elpased * self.fps) % self.frame_count
        self.image.clip_draw(index * self.width, 0, self.width, self.height, self.x, self.y)

