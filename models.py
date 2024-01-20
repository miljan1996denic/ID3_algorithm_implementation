class Node:
    def __init__(self, table, name):
        self.table = table
        self.name = name
        self.children = []
        self.branches = []

    def set_name(self, name):
        self.name = name

    def add_child(self, child):
        self.children.append(child)

    def add_branch(self, branch):
        self.branches.append(branch)

    def add_child_and_branch(self, child, branch):
        self.children.append(child)
        self.branches.append(branch)


class TerminalNode(Node):
    def __init__(self, table, name):
        Node.__init__(self, table, name)