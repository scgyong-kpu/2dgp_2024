from heapdict import heapdict # pip install heapdict 필요하다.

eight_ways = [
    (-1,-1, 14), (0,-1, 10), (1,-1, 14),
    (-1, 0, 10),             (1, 0, 10),
    (-1, 1, 14), (0, 1, 10), (1, 1, 14),
]

class AStarNode:
    def __init__(self, x, y, g, h, parent=None):
        self.x, self.y = x, y
        self.g, self.h = g, h
        self.f = g + h
        self.parent = parent

    def __lt__(self, other):
        return self.f < other.f

class AStarPath:
    def __init__(self, start_tuple, end_tuple):
        self.start = start_tuple
        self.end = end_tuple
        self.open_list = heapdict()
        self.close_list = dict()

        sx, sy = start_tuple
        h = self.heuristic_cost(sx, sy)
        start_node = AStarNode(sx, sy, 0, h)
        self.open_list[start_tuple] = start_node

    def heuristic_cost(self, x, y):
        ex, ey = self.end
        dist = abs(ex - x) + abs(ey - y)
        return dist * 10

    def is_wall(self, x, y):
        return False

    def find_tiles(self):
        while self.open_list:
            curr_pos, curr_node = self.open_list.popitem()
            x,y = curr_pos
            self.close_list[curr_pos] = curr_node
            if curr_pos == self.end:
                break
            for dx,dy,co in eight_ways:
                new_pos = x+dx, y+dy
                if self.is_wall(*new_pos): continue
                if new_pos in self.close_list: continue
                g = curr_node.g + co
                if new_pos in self.open_list:
                    node = self.open_list[new_pos]
                    if node.g > g:
                        node.parent = curr_node
                        node.f, node.g = g + node.h, g
                else:
                    h = self.heuristic_cost(*new_pos)
                    node = AStarNode(*new_pos, g, h, curr_node)
                    self.open_list[new_pos] = node

        path = []
        pos = self.end
        if not pos in self.close_list:
            return path
        node = self.close_list[pos]
        while node:
            path.append( (node.x, node.y) )
            node = node.parent
        path.reverse()
        return path
