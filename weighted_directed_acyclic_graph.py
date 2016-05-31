from random import shuffle


class Node:

    def __init__(self, label, direct_successors_and_edge_weights=[], color=None):
        self.label = label
        self.direct_successors_and_edge_weights = direct_successors_and_edge_weights
        self.visited = False
        self.shortest_path_value = float('inf')
        self.shortest_path_predecessor = None


a = Node('A')
b = Node('B')
c = Node('C')
d = Node('D')
e = Node('E')
f = Node('F')

a.direct_successors_and_edge_weights = [(b, 2), (c, 4)]
b.direct_successors_and_edge_weights = [(d, 1), (e, 6)]
c.direct_successors_and_edge_weights = [(e, 9), (f, 3)]
d.direct_successors_and_edge_weights = []
e.direct_successors_and_edge_weights = [(d, 7)]
f.direct_successors_and_edge_weights = []

graph_a = [a, b, c, d, e, f]


g = Node('G')
h = Node('H')
i = Node('I')
j = Node('J')
k = Node('K')
l = Node('L')
m = Node('M')

g.direct_successors_and_edge_weights = [(h, 1), (i, 1), (l, 1)]
h.direct_successors_and_edge_weights = [(k, 1)]
i.direct_successors_and_edge_weights = []
j.direct_successors_and_edge_weights = [(i, 1), (k, 1), (l, 1), (m, 1)]
k.direct_successors_and_edge_weights = []
l.direct_successors_and_edge_weights = [(i, 1)]
m.direct_successors_and_edge_weights = [(g, 1), (k, 1)]

graph_b = [g, h, i, j, k, l, m]


def topological_sort(graph):

    topologically_sorted_graph = []

    def dfs(node):
        node.visited = True
        for direct_successor, edge_weight in node.direct_successors_and_edge_weights:
            if not direct_successor.visited:
                dfs(direct_successor)
        # O(n)!
        topologically_sorted_graph.insert(0, node)

    for node in graph:
        if not node.visited:
            dfs(node)

    return topologically_sorted_graph


def shortest_path(graph, start_node, target_node):

    start_node.shortest_path_value = 0

    # start with start_node
    for node in graph:

        for direct_successor, edge_weight in node.direct_successors_and_edge_weights:

            if direct_successor.shortest_path_value > node.shortest_path_value + edge_weight:
                direct_successor.shortest_path_value = node.shortest_path_value + edge_weight
                direct_successor.shortest_path_predecessor = node

    shortest_path_nodes = [target_node]

    current_node = target_node
    while current_node.shortest_path_predecessor:

        # O(n)!
        shortest_path_nodes.insert(0, current_node.shortest_path_predecessor)
        current_node = current_node.shortest_path_predecessor

    return shortest_path_nodes


def is_topologically_sorted(graph):
    for node in graph:
        for direct_successor, edge_weight in node.direct_successors_and_edge_weights:
            if graph.index(node) > graph.index(direct_successor):
                return False
    return True


def reset(graph):
    for node in graph:
        node.visited = False
        node.shortest_path_value = float('inf')
        node.shortest_path_predecessor = None


graph_tests = [
    (graph_a, graph_a[0], graph_a[4], [a, b, e]),
    (graph_b, graph_b[0], graph_b[2], [g, i]),
]


def test_graphs():

    for graph, start_node, target_node, expected_shortest_path in graph_tests:

        for _ in xrange(100):

            reset(graph)

            shuffle(graph)

            topologically_sorted_graph = topological_sort(graph)

            if not is_topologically_sorted(topologically_sorted_graph):
                print 'NOT TOPOLOGICALLY SORTED'
                break

            if shortest_path(topologically_sorted_graph, start_node, target_node) != expected_shortest_path:
                print 'NOT SHORTEST PATH'
                break

        reset(graph)

test_graphs()
