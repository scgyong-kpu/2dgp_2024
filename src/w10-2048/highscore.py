import pickle
import os
import time
from gfw import *

import sys
self = sys.modules[__name__]

FILENAME = 'score.pickle'

class Entry:
    def __init__(self, score):
        self.score = score
        self.time = time.localtime()
    def timestr(self):
        return time.strftime('%Y-%m-%d %H:%M:%S', self.time)

def load():
    global font
    font = gfw.font.load('res/ConsolaMalgun.ttf')

    global scores
    try:
        f = open(FILENAME, "rb")
        scores = pickle.load(f)
        f.close()
        # print("Scores:", scores)
    except:
        print("No highscore file")
        scores = [ ]

def add(score):
    global last_entry
    last_entry = Entry(score)

    global scores
    scores.append(last_entry)
    scores.sort(key=lambda e:e.score, reverse=True)
    scores = scores[:10]
    try:
        with open(FILENAME, "wb") as f:
            pickle.dump(scores, f)
    except:
        pass

def draw():
    global font, last_rank
    no = 1
    y = 360
    for e in scores:
        str = "{:2d} {:10d}".format(no, e.score)
        color = (255, 255, 128) if e == last_entry else (223, 255, 223)
        font.draw(30, y, str, color)
        font.draw(220, y, e.timestr(), color)
        y -= 30
        no += 1


def update():
    pass
