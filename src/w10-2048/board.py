import random

CX_BLOCK = 4
CY_BLOCK = 4

class Board:
    def __init__(self):
        self.blocks = [ [ None for _ in range(CX_BLOCK) ] for _ in range(CY_BLOCK) ]

    def clear(self):
        for y in range(CY_BLOCK):
            for x in range(CX_BLOCK):
                block = self.get_block(x, y)
                if block is not None:
                    block.remove()

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

    def generate_block(self, block):
        positions = []
        for y in range(CY_BLOCK):
            for x in range(CX_BLOCK):
                if self.get_block(x, y) is None:
                    positions.append( (x, y) )
        if len(positions) == 0:
            print('No black space')
            return None
        pos = random.choice(positions)
        print(f'Generating {block} @{pos}')
        self.set_block(*pos, block)
        return pos

    def is_full(self):
        for y in range(CY_BLOCK):
            for x in range(CX_BLOCK):
                if self.get_block(x, y) is None:
                    return False
        return True

    def move_left(self):
        moved = False
        for y in range(4):
            for x in range(4):
                ox, oy = (x, y)
                b = self.get_block(ox, oy)
                if b is None:
                    for x2 in range(x + 1, 4):
                        ox2, oy2 = (x2, y)
                        b = self.get_block(ox2, oy2)
                        # v = self.blocks[y * 4 + x2].getValue()
                        if b is not None:
                            self.set_block(ox, oy, b)
                            b.move_to(ox, oy)
                            self.set_block(ox2, oy2, None)
                            moved = True
                            break
                    if b is None:
                        break

def test_board():
    board = Board()
    for i in range(17):
        block = random.choice([2, 4])
        board.generate_block(block)
        print('full =', board.is_full())
        board.print_blocks()

if __name__ == '__main__':
    test_board()

