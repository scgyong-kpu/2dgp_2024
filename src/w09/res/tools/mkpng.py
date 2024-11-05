import os
from PIL import Image, ImageDraw, ImageFont

# adjs = {
#     1: (0, 4),
# }

for char_index in range(1, 11): #, (ax, ay) in adjs.items():

    out = Image.new("RGBA", (2800, 100), '#0000')

    x = 0
    for frame_index in range(28):
        fname = f'l_{char_index:02d}_{frame_index:02d}.png'
        with Image.open(fname) as im:
            w, h = im.size
            if w >= h:
                h = round(100 * h / w)
                w = 100
                ax = 0
                ay = (w - h) // 2
            else:
                w = round(100 * w / h)
                h = 100
                ax = (h - w) // 2
                ay = 0
            out.paste(im.resize((w, h)), (x + ax, ay))
        x += 100

    out.save(f'../lol/f_{char_index:02}.png')



    # print(char_index, frame_index)
