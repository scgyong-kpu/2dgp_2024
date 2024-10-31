import json

icon_cmd = "curl 'https://www.spriters-resource.com/resources/sheet_icons/%s/%s.png' > out/%s_icon.png"
sheet_cmd = "curl 'https://www.spriters-resource.com/resources/sheets/%s/%s.png' > out/%s_sheet.png"

with open('out/cookies.json', 'r') as f:
    cookies = json.load(f)

for cookie in cookies:
    grade, number = cookie['grade'], cookie['id']
    print(icon_cmd % (grade, number, number))
    print(sheet_cmd % (grade, number, number))

'''

curl 'https://www.spriters-resource.com/resources/sheet_icons/104/107566.png' > out/107566_icon.png
curl 'https://www.spriters-resource.com/resources/sheets/104/107566.png' > out/107566_sheet.png
curl 'https://www.spriters-resource.com/resources/sheet_icons/104/107567.png' > out/107567_icon.png
curl 'https://www.spriters-resource.com/resources/sheets/104/107567.png' > out/107567_sheet.png
curl 'https://www.spriters-resource.com/resources/sheet_icons/104/107571.png' > out/107571_icon.png
curl 'https://www.spriters-resource.com/resources/sheets/104/107571.png' > out/107571_sheet.png
...

'''

