# legally color a simple graph (undirected, no multiple edges or loops)
# use D+1 or less colors, where D is the maximum degree


# nodes are represented by a list of node objects that have a label,
# a list of neighbors, and a color (effectively an adjacency list)

class Node:

    def __init__(self, label):
        self.label = label
        self.neighbors = []
        self.color = None


# brute force
#
# try every possible combination of colors until we find a legal coloring
#
# time:   O(C^N * N+M)  where C is the number of colors and N is the number of nodes. this is
#                       effectively O(N^N) in a graph where one node connects to all other nodes
#                       because D would be N-1 and C is defined as D+1
# space:  O(1)          itertools.product is an iterator

import itertools

def color_graph_brute_force(graph, colors):

    # get the cartesian product of all the colors, for every node
    # (every color for every color, for as many nodes as we need to color)
    for current_coloring in itertools.product(colors, repeat=len(graph)):

        # assign current coloring to all nodes
        for index, node in enumerate(graph):
            node.color = current_coloring[index]

        if is_graph_legally_colored(graph):
            break


# greedy
#
# with ordered nodes and colors, color each node with the first color that's legal
#
# time:   O(N+M)  where N is the number of nodes and M is the number of edges.
#                 but M is triangular series of N-1 in a complete graph (every node
#                 connected) so can be O(N^2). M is useful because it more closely
#                 gives the big o for all graphs, not just complete graphs
# space:  O(D)    we need to track the illegal colors for a node, which is at most
#                 all of the colors except 1, or the maximum degree, which in the
#                 worse case in N-1

def color_graph_greedy(graph, colors):

    for node in graph:

        illegal_colors = set([neighbor.color for neighbor in node.neighbors if neighbor.color])

        for color in colors:
            if color not in illegal_colors:
                node.color = color
                break


# tests

def is_graph_legally_colored(graph):

    for node in graph:
        for neighbor in node.neighbors:
            if (node.color == neighbor.color) or (not node.color):
                return False
    return True


a = Node('A')
b = Node('B')
c = Node('C')
d = Node('D')
e = Node('E')
f = Node('F')

a.neighbors = [b, d]
b.neighbors = [a, c, d]
c.neighbors = [b, e, f]
d.neighbors = [a, b]
e.neighbors = [c]
f.neighbors = [c]


g = Node('G')
h = Node('H')
i = Node('I')
j = Node('J')
k = Node('K')
l = Node('L')

g.neighbors = [j, l]
h.neighbors = [i, k]
i.neighbors = [h, l]
j.neighbors = [g, k]
k.neighbors = [h, j]
l.neighbors = [g, i]


m = Node('M')
n = Node('N')
o = Node('O')
p = Node('P')

m.neighbors = [n]
n.neighbors = [m, o]
o.neighbors = [n, p]
p.neighbors = [o]


q = Node('Q')
r = Node('R')
s = Node('S')
t = Node('T')
u = Node('U')

q.neighbors = [r, s, t, u]
r.neighbors = [q, s, t, u]
s.neighbors = [q, r, t, u]
t.neighbors = [q, r, s, u]
u.neighbors = [q, r, s, t]


graphs = [
    [a, b, c, d, e, f],
    [g, h, i, j, k, l],
    [m, n, o, p],
    [q, r, s, t, u],
]

coloring_algorithms = [
    color_graph_brute_force,
    color_graph_greedy,
]


colors = ['red', 'yellow', 'green', 'blue', 'purple', 'white']

for coloring_algorithm in coloring_algorithms:
    for graph in graphs:

        d = max([len(node.neighbors) for node in graph])
        d_plus_one_colors = colors[:d + 1]

        for node in graph:
            node.color = None

        coloring_algorithm(graph, d_plus_one_colors)

        if not is_graph_legally_colored(graph):
            raise Exception('Not legally colored')
