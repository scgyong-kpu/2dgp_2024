import gfw_loop
from grass import Grass

gfw_loop.game_objects.append(Grass())

gfw_loop.start()

''' 실행결과:
Pico2d is prepared.
Traceback (most recent call last):
  File "D:/Lectures/2024_2/2dgp/git/src/w04/w04_1.py", line 4, in <module>
    gfw_loop.game_objects.append(Grass())
  File "D:/Lectures/2024_2/2dgp/git/src/w04/grass.py", line 5, in __init__
    self.image = load_image('grass.png')
  File "C:/Users/scgyong/AppData/Local/Programs/Python/Python39/lib/site-packages/pico2d/pico2d.py", line 346, in load_image
    texture = IMG_LoadTexture(renderer, name.encode('UTF-8'))
NameError: name 'renderer' is not defined
'''

''' 
  그렇다고 start 뒤에 Grass 객체를 생성하는 것도 말이 되지 않는다
  start() 함수는 게임루프가 종료한 뒤에나 리턴하기 때문이다
'''

