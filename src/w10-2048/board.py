import random

BOARD_SIZE = 4

class Board:
    def __init__(self):
        self.blocks = [ [ None for _ in range(BOARD_SIZE) ] for _ in range(BOARD_SIZE) ]

    def clear(self):
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                block = self.get_block(x, y)
                if block is not None:
                    block.remove()

        self.blocks = [ [ None for _ in range(BOARD_SIZE) ] for _ in range(BOARD_SIZE) ]

    def get_block(self, x, y):
        return self.blocks[y][x]

    def set_block(self, x, y, block):
        self.blocks[y][x] = block

    def print_blocks(self):
        for y in range(BOARD_SIZE - 1, -1, -1):
            line = ''
            for x in range(BOARD_SIZE):
                b = self.get_block(x, y)
                txt = '[      ] ' if b is None else f'[{b:^6d}] '
                line += txt
            print(line)

    def generate_block(self, block):
        positions = []
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
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
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                if self.get_block(x, y) is None:
                    return False
        return True

    def move_left(self):
        self.move(lambda x,y: (x,y))

    def move_right(self):
        self.move(lambda x,y: (BOARD_SIZE - x - 1, y))

    def move_down(self):
        self.move(lambda x,y: (y,x))

    def move_up(self):
        self.move(lambda x,y: (BOARD_SIZE - y - 1, BOARD_SIZE - x - 1))

    def move(self, converter):
        moved = False
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                ox, oy = converter(x, y)
                b = self.get_block(ox, oy)
                if b is None:
                    for x2 in range(x + 1, BOARD_SIZE):
                        ox2, oy2 = converter(x2, y)
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

