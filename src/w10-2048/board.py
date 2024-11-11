
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

def test_board():
    board = Board()
    board.set_block(2, 3, 16)
    board.set_block(1, 2, 4)
    board.set_block(0, 2, 8)
    board.set_block(3, 0, 32)
    board.print_blocks()

if __name__ == '__main__':
    test_board()

