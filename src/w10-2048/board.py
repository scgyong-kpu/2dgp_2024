
blocks = [ [ None for _ in range(4) ] for _ in range(4) ]

def get_block(x, y):
    return blocks[y][x]

def set_block(x, y, block):
    blocks[y][x] = block

def print_blocks():
    for y in range(3, -1, -1):
        line = ''
        for x in range(4):
            b = get_block(x, y)
            txt = '[      ] ' if b is None else f'[{b:^6d}] '
            line += txt
        print(line)

def test_board():
    set_block(2, 3, 16)
    set_block(1, 2, 4)
    set_block(0, 2, 8)
    set_block(3, 0, 32)
    print_blocks()

if __name__ == '__main__':
    test_board()

