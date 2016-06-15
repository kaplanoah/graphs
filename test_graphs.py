import random
from collections import defaultdict

from coloring import Node, color_graph_brute_force, color_graph_greedy, is_graph_legally_colored
from weighted_directed_acyclic_graph import TopologicalOrderDfs, topological_order_kahns, shortest_path as topological_shortest_path
from unweighted_undirected_cyclic_graph import shortest_path_bfs


def build_weighted_directed_graph(nodes, edges):

    graph = {node: [] for node in nodes}

    for predecessor, successor, weight in edges:
        graph[predecessor].append((successor, weight))

    return graph


def build_unweighted_undirected_graph(nodes, edges):

    graph = {node: [] for node in nodes}

    for node_1, node_2, weight in edges:
        for node_a, node_b in ((node_1, node_2), (node_2, node_1)):
            if node_b not in graph[node_a]:
                graph[node_a].append(node_b)

    return graph


def build_unweighted_undirected_colored_graph(labels, edges):

    graph = [Node(label) for label in labels]

    for label_1, label_2, weight in edges:
        for label_a, label_b in ((label_1, label_2), (label_2, label_1)):

            for node in graph:
                if node.label == label_a:
                    out_node = node
                if node.label == label_b:
                    in_node = node

            if in_node not in out_node.neighbors:
                out_node.neighbors.append(in_node)

    return graph


graph_types = {
    'weighted_directed':             build_weighted_directed_graph,
    'unweighted_undirected':         build_unweighted_undirected_graph,
    'unweighted_undirected_colored': build_unweighted_undirected_colored_graph,
}


test_graphs = defaultdict(dict)

shortest_paths = {}

impossible_to_color_graphs = set()

cyclic_graphs = set()


nodes = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

test = None # test name


def build_graphs(edges):
    for graph_type, build_graph_type in graph_types.iteritems():
        test_graphs[test][graph_type] = build_graph_type(nodes, edges)


def insert_shortest_path_tests(start_node, target_node, first_shortest_path, second_shortest_path):
    shortest_paths[test] = {
        1: (start_node, target_node, first_shortest_path),
        2: (start_node, target_node, second_shortest_path),
    }


test = 'disconnected'

build_graphs([])
insert_shortest_path_tests('A', 'D', [], [])


test = 'line'

build_graphs([('A', 'B', 6), ('B', 'C', 9), ('C', 'D', 4), ('D', 'E', 7), ('E', 'F', 4),
              ('F', 'G', 1)])
insert_shortest_path_tests('D', 'G', ['D', 'E', 'F', 'G'], [])


test = 'leaf'

build_graphs([('A', 'B', 1), ('A', 'C', 4), ('B', 'D', 2), ('C', 'E', 3), ('D', 'F', 7),
              ('E', 'G', 1)])
insert_shortest_path_tests('A', 'D', ['A', 'B', 'D'], [])


test = 'tree'

build_graphs([('A', 'B', 2), ('A', 'C', 9), ('B', 'D', 3), ('B', 'E', 1), ('C', 'F', 4),
              ('E', 'G', 2)])
insert_shortest_path_tests('A', 'G', ['A', 'B', 'E', 'G'], [])


test = 'cycle'

build_graphs([('A', 'B', 6), ('B', 'C', 9), ('C', 'D', 4), ('D', 'E', 7), ('E', 'F', 4),
              ('F', 'G', 1), ('G', 'A', 9)])
insert_shortest_path_tests('B', 'D', ['B', 'C', 'D'], [])
cyclic_graphs.add(test)


test = 'cyclic'

build_graphs([('A', 'B', 1), ('A', 'C', 3), ('A', 'D', 7), ('B', 'C', 3), ('C', 'A', 9),
              ('D', 'E', 4), ('D', 'F', 5), ('E', 'F', 3), ('F', 'E', 2), ('F', 'G', 9)])
insert_shortest_path_tests('A', 'F', ['A', 'D', 'F'], ['A', 'D', 'E', 'F'])
cyclic_graphs.add(test)


test = 'loop'

build_graphs([('A', 'B', 4), ('B', 'B', 5), ('B', 'C', 9)])
insert_shortest_path_tests('A', 'C', ['A', 'B', 'C'], ['A', 'B', 'B', 'C'])
impossible_to_color_graphs.add(test)
cyclic_graphs.add(test)


test = 'complete/nonplanar'

edges = [('D', 'B', 1), ('D', 'C', 1), ('C', 'B', 1)]
for node in nodes:
    for neighbor in nodes:
        if (node != neighbor) and ((node, neighbor) not in [('D', 'B'), ('D', 'C'), ('C', 'B')]):
            edges.append((node, neighbor, random.randint(3, 9)))
build_graphs(edges)
insert_shortest_path_tests('D', 'B', ['D', 'B'], ['D', 'C', 'B'])
cyclic_graphs.add(test)


test = 'wheel center'

build_graphs([('A', 'B', 1), ('A', 'C', 4), ('A', 'D', 2), ('A', 'E', 6), ('A', 'F', 3),
              ('A', 'G', 3), ('B', 'C', 3), ('C', 'D', 3), ('D', 'E', 5), ('E', 'F', 8),
              ('F', 'G', 8), ('G', 'B', 2)])
insert_shortest_path_tests('A', 'E', ['A', 'E'], ['A', 'D', 'E'])
cyclic_graphs.add(test)


test = 'wheel outside'

build_graphs([('A', 'B', 1), ('A', 'C', 4), ('A', 'D', 2), ('A', 'E', 6), ('A', 'F', 3),
              ('A', 'G', 3), ('B', 'C', 3), ('C', 'D', 3), ('D', 'E', 5), ('E', 'F', 8),
              ('F', 'G', 8), ('G', 'B', 2)])
insert_shortest_path_tests('F', 'G', ['F', 'G'], ['F', 'A', 'G'])
cyclic_graphs.add(test)


test = 'star'

build_graphs([('A', 'B', 5), ('A', 'C', 6), ('A', 'D', 3), ('A', 'E', 7), ('A', 'F', 1),
              ('A', 'G', 2)])
insert_shortest_path_tests('A', 'D', ['A', 'D'], [])


test = 'bipartitie'

build_graphs([('A', 'F', 4), ('B', 'E', 2), ('B', 'G', 3), ('C', 'F', 6), ('C', 'G', 3),
              ('D', 'E', 3), ('D', 'G', 3), ('E', 'B', 3), ('G', 'C', 3), ('G', 'D', 3)])
insert_shortest_path_tests('D', 'F', ['D', 'G', 'C', 'F'], ['D', 'E', 'B', 'G', 'C', 'F'])
cyclic_graphs.add(test)




coloring_algorithms = [
    color_graph_brute_force,
    color_graph_greedy,
]

colors = ['red', 'yellow', 'green', 'blue', 'purple', 'white', 'orange', 'black']

for coloring_algorithm in coloring_algorithms:
    print coloring_algorithm.__name__

    for test_name, graph_types in test_graphs.iteritems():
        print '\t%s' % test_name

        graph = graph_types['unweighted_undirected_colored']

        d = max([len(node.neighbors) for node in graph])
        d_plus_one_colors = colors[:d + 1]

        for node in graph:
            node.color = None

        coloring_algorithm(graph, d_plus_one_colors)

        expected_colored = True
        if test_name in impossible_to_color_graphs:
            expected_colored = False

        if is_graph_legally_colored(graph) != expected_colored:
            raise Exception('Not legally colored: %s' % test_name)


topological_ordering_algorithms = [
    TopologicalOrderDfs,
    topological_order_kahns,
]

def is_topologically_ordered(graph, topologically_ordered_nodes):
    for node, direct_successors in graph.iteritems():
        for direct_successor, edge_weight in direct_successors:
            if topologically_ordered_nodes.index(node) > topologically_ordered_nodes.index(direct_successor):
                return False
    return True

for topological_ordering_algorithm in topological_ordering_algorithms:
    print topological_ordering_algorithm.__name__

    for test_name, graph_types in test_graphs.iteritems():
        print '\t%s' % test_name

        if test_name in cyclic_graphs:
            print '\tSKIPPING'
            continue

        graph = graph_types['weighted_directed']

        start_node, target_node, shortest_path = shortest_paths[test_name][1]

        try:
            topologically_ordered_nodes = topological_ordering_algorithm(graph).order_graph()
        except AttributeError:
            topologically_ordered_nodes = topological_ordering_algorithm(graph)

        if not is_topologically_ordered(graph, topologically_ordered_nodes):
            raise Exception('Not topologically ordered: %s' % test_name)

    if topological_shortest_path(graph, topologically_ordered_nodes, start_node, target_node) != shortest_path:
        raise Exception('Not shortest path: %s' % test_name)


print 'shortest_path_bfs'

for test_name, graph_types in test_graphs.iteritems():
    print '\t%s' % test_name

    graph = graph_types['unweighted_undirected']

    start_node, target_node, shortest_path = shortest_paths[test_name][1]

    if shortest_path_bfs(graph, start_node, target_node) != shortest_path:
        print shortest_path_bfs(graph, start_node, target_node), shortest_path
        raise Exception('Not shortest path: %s' % test_name)
