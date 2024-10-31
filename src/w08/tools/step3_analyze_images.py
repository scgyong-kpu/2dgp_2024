import json
import pico2d

with open('out/cookies.json', 'r') as f:
    cookies = json.load(f)

pico2d.open_canvas()

for cookie in cookies:
    cid = cookie['id']
    fname = f'out/{cid}_sheet.png'
    try:
        image = pico2d.load_image(fname)
        print(f'{fname=}, w={image.w}, h={image.h}')
        del image
    except:
        pass # ignore error files

pico2d.close_canvas()

