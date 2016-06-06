from itertools import product


class Node:

    def __init__(self, label, neighbors=[], color=None):
        self.label = label
        self.neighbors = neighbors
        self.color = color


def color_graph_brute_force(graph, colors):

    for color_combination in product(colors, repeat=len(graph)):

        for index, node in enumerate(graph):
            node.color = color_combination[index]

        if is_graph_legally_colored(graph):
            return graph


def color_graph_backtracking(graph, colors):

    # implement

    return graph


def color_graph_greedy(graph, colors):

    for node in graph:

        illegal_colors = set([neighbor.color for neighbor in node.neighbors])

        for color in colors:
            if color not in illegal_colors:
                node.color = color
                break


def is_graph_legally_colored(graph):

    for node in graph:

        illegal_colors = set([neighbor.color for neighbor in node.neighbors])

        if (not node.color) or (node.color in illegal_colors):
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


k = Node('K')
l = Node('L')
m = Node('M')
n = Node('N')

k.neighbors = [l]
l.neighbors = [k, m]
m.neighbors = [l, n]
n.neighbors = [m]


graphs = [
    [a, b, c, d, e, f],
    [g, h, i, j, k, l],
    [k, l, m, n],
]

coloring_algorithms = [
    color_graph_brute_force,
    color_graph_backtracking,
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
