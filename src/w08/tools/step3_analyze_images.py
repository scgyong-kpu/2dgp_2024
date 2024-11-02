import json
import pico2d

with open('out/cookies.json', 'r') as f:
    cookies = json.load(f)

pico2d.open_canvas()

# 1.666, 1.333 = pet. 2.000 = 14x7
sizes = [
  (11, 6), (13, 6), (15, 7), (15, 6), (15, 5)
]

# for cx,cy in sizes:
#   print(f'ratio = {cx/cy:.3f}')
# exit()

cookie_chars = []

for cookie in cookies:
    cid = cookie['id']
    fname = f'out/{cid}_sheet.png'
    try:
        image = pico2d.load_image(fname)
        ratio = (image.w - 2) / (image.h - 2)

    except:
        continue # ignore error files

    for cx, cy in sizes:
        if ratio == cx / cy:
            break
    else:
        print(f'Not processing: {cookie["name"]} id={cid} ratio={ratio:.3f}')
        continue

    sprite_type = f'{cx}x{cy}'
    cell_size = (image.w - 2) // cx - 2
    # print(f'{sprite_type=} {cell_size=}')
    cookie["type"] = sprite_type
    cookie["size"] = cell_size
    del cookie["grade"]

    print(cookie)

    cookie_chars.append(cookie)

pico2d.close_canvas()

with open('out/cookie_chars.json', 'w') as f:
    json.dump(cookie_chars, f, indent=2)



'''

[
  {
    "id": "107566",
    "name": "Brave Cookie",
    "type": "11x6",
    "size": 270
  },
  {
    "id": "107567",
    "name": "Bright Cookie",
    "type": "11x6",
    "size": 288
  },

...

'''
