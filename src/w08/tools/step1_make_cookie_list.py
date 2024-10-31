import re

pat = re.compile(r'\s+<img src="/resources/sheet_icons/(\d+)/(\d+).png[^"]*" alt="([^"]+)"[^>]*>\s*$')

with open('out/cookierun.html', 'r') as f:
    while True:
        str = f.readline()
        if not str: break

        m = pat.match(str)
        if not m: continue
        grade, number, name = m.groups()
        char = { "id": number, "name": name, "grade": grade }
        print(char)


