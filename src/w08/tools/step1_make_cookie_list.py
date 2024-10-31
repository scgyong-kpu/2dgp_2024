line = 0
with open('out/cookierun.html', 'r') as f:
    while True:
        str = f.readline()
        if not str: break

        line += 1

print(f'{line} lines read.')

