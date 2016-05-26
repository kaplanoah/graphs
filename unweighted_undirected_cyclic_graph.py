
class Node:

    def __init__(self, label, neighbors=[], color=None):
        self.label = label
        self.neighbors = neighbors


a = Node('A')
b = Node('B')
c = Node('C')
d = Node('D')
e = Node('E')
f = Node('F')

a.neighbors = [b, c]
b.neighbors = [a, d, e]
c.neighbors = [a, f]
d.neighbors = [b, e]
e.neighbors = [b, d]
f.neighbors = [c]

graph = [a, b, c, d, e, f]