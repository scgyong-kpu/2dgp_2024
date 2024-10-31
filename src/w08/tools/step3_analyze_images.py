import json
import pico2d

with open('out/cookies.json', 'r') as f:
    cookies = json.load(f)

pico2d.open_canvas()

ratios = dict()

for cookie in cookies:
    cid = cookie['id']
    fname = f'out/{cid}_sheet.png'
    try:
        image = pico2d.load_image(fname)
        ratio = (image.w - 2) / (image.h - 2)
        if ratio in ratios:
            ratios[ratio] += 1
        else:
            ratios[ratio] = 1
        print(f'{fname=}, w={image.w}, h={image.h} {ratio=:.3f} count={ratios[ratio]}')
        del image
    except:
        pass # ignore error files

pico2d.close_canvas()

counts = list(ratios.items())
counts.sort(key=lambda item: -item[1])

print(counts)

'''

Pico2d is prepared.
fname='out/107566_sheet.png', w=2994, h=1634 ratio=1.833 count=1
fname='out/107567_sheet.png', w=3192, h=1742 ratio=1.833 count=2
fname='out/107571_sheet.png', w=3544, h=1934 ratio=1.833 count=3
fname='out/107570_sheet.png', w=3544, h=1934 ratio=1.833 count=4
fname='out/107569_sheet.png', w=5192, h=2078 ratio=2.500 count=1
...

[(1.6, 48), (1.3333333333333333, 17), (2.5, 12), (1.8333333333333333, 10), (2.1666666666666665, 7),
 (3.0, 4), (2.142857142857143, 4), (1.1428571428571428, 4), (2.0, 3), (1.875, 3), 
 (2.3333333333333335, 2), (2.4, 2), (3.4, 2), (0.7152317880794702, 2),
...

'''
