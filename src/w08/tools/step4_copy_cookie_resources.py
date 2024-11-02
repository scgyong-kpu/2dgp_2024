import json
import os
import shutil

try:
    os.mkdir('../res/cookies/')
except:
    pass

with open('out/cookie_chars.json', 'r') as f:
    chars = json.load(f)

for cookie in chars:
    cid = cookie["id"]
    shutil.copyfile(f'out/{cid}_icon.png', f'../res/cookies/{cid}_icon.png')
    shutil.copyfile(f'out/{cid}_sheet.png', f'../res/cookies/{cid}_sheet.png')

shutil.copyfile('out/cookie_chars.json', '../res/cookies.json')
