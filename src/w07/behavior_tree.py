BT_FAIL, BT_SUCCESS, BT_RUNNING = range(3)

class LeafNode:
    def __init__(self, name, func):
        self.name = name
        self.func = func
    def run(self):
        return self.func()

class BranchNode:
    def __init__(self, name, children=[]):
        self.name = name
        self.children = children
        self.prev_running_pos = 0
    def add_child(self, child):
        self.children.append(child)
    def add_children(self, *children):
        for child in children:
            self.children.append(child)
    def run_children(self, ret_val_if, def_val):
        for i in range(self.prev_running_pos, len(self.children)):
            child = self.children[i]
            value = child.run()
            if value == BT_RUNNING:
                self.prev_running_pos = i
                return BT_RUNNING
            if value == ret_val_if:
                return ret_val_if
        self.prev_running_pos = 0
        return def_val

class Selector(BranchNode):
    def run(self):
        self.run_children(BT_SUCCESS, BT_FAIL)

class Sequence(BranchNode):
    def run(self):
        self.run_children(BT_FAIL, BT_SUCCESS)

class BehaviorTree:
    def __init__(self, root):
        self.root = root
    def run(self):
        self.root.run()
