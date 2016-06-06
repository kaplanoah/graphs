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
            break


class ColorGraphBacktrackingDfs:

    def __init__(self, graph, colors):
        self.graph = graph
        self.colors = colors

    def color_graph(self):

        self.visited_nodes = set()

        for node in self.graph:
            if node not in self.visited_nodes:
                self.color_node_dfs(node)

    def color_node_dfs(self, node):

        illegal_colors = set([neighbor.color for neighbor in node.neighbors])

        for color in self.colors:
            if color not in illegal_colors:
                node.color = color
                break

        self.visited_nodes.add(node)

        for neighbor in node.neighbors:
            if neighbor not in self.visited_nodes:
                self.color_node_dfs(neighbor)


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


m = Node('M')
n = Node('N')
o = Node('O')
p = Node('P')

m.neighbors = [n]
n.neighbors = [m, o]
o.neighbors = [n, p]
p.neighbors = [o]


graphs = [
    [a, b, c, d, e, f],
    [g, h, i, j, k, l],
    [m, n, o, p],
]

coloring_algorithms = [
    color_graph_brute_force,
    ColorGraphBacktrackingDfs,
    color_graph_greedy,
]


colors = ['red', 'yellow', 'green', 'blue', 'purple', 'white']

for coloring_algorithm in coloring_algorithms:
    for graph in graphs:

        d = max([len(node.neighbors) for node in graph])
        d_plus_one_colors = colors[:d + 1]

        for node in graph:
            node.color = None

        try:
            coloring_algorithm(graph, d_plus_one_colors).color_graph()
        except AttributeError:
            coloring_algorithm(graph, d_plus_one_colors)

        if not is_graph_legally_colored(graph):
            raise Exception('Not legally colored')
