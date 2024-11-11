import random

CX_BLOCK = 4
CY_BLOCK = 4

class Board:
    def __init__(self):
        self.blocks = [ [ None for _ in range(CX_BLOCK) ] for _ in range(CY_BLOCK) ]

    def get_block(self, x, y):
        return self.blocks[y][x]

    def set_block(self, x, y, block):
        self.blocks[y][x] = block

    def print_blocks(self):
        for y in range(CY_BLOCK - 1, -1, -1):
            line = ''
            for x in range(CX_BLOCK):
                b = self.get_block(x, y)
                txt = '[      ] ' if b is None else f'[{b:^6d}] '
                line += txt
            print(line)

    def generate_block(self):
        positions = []
        for y in range(CY_BLOCK):
            for x in range(CX_BLOCK):
                if self.get_block(x, y) is None:
                    positions.append( (x, y) )
        if len(positions) == 0:
            print('No black space')
            return False
        block = random.choice([2, 4])
        pos = random.choice(positions)
        print(f'Generating {block} @{pos}')
        self.set_block(*pos, block)
        return True


def test_board():
    board = Board()
    for i in range(16):
        board.generate_block()
        board.print_blocks()

if __name__ == '__main__':
    test_board()

