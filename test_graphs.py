from coloring import Node, color_graph_brute_force, color_graph_greedy, is_graph_legally_colored

from collections import defaultdict



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

graphs_impossible_to_color = set()


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
insert_shortest_path_tests('A', 'D', None, None)


test = 'leaf'

build_graphs([('A', 'B', 1), ('A', 'C', 4), ('B', 'D', 2), ('C', 'E', 3), ('D', 'F', 7),
              ('E', 'G', 1)])
insert_shortest_path_tests('A', 'D', ['A', 'B', 'D'], None)


test = 'tree'

build_graphs([('A', 'B', 2), ('A', 'C', 9), ('B', 'D', 3), ('B', 'E', 1), ('C', 'F', 4),
              ('E', 'G', 2)])
insert_shortest_path_tests('A', 'G', ['A', 'B', 'E', 'G'], None)


test = 'cycle'

build_graphs([('A', 'B', 6), ('B', 'C', 9), ('C', 'D', 4), ('D', 'E', 7), ('E', 'F', 4),
              ('F', 'G', 1), ('G', 'A', 9)])
insert_shortest_path_tests('B', 'D', ['B', 'C', 'D'], None)


test = 'cyclic'

build_graphs([('A', 'B', 1), ('A', 'C', 3), ('A', 'D', 7), ('B', 'C', 3), ('C', 'A', 9),
              ('D', 'E', 4), ('D', 'F', 5), ('E', 'F', 3), ('F', 'E', 2), ('F', 'G', 9)])
insert_shortest_path_tests('A', 'F', ['A', 'D', 'F'], ['A', 'D', 'E', 'F'])


test = 'loop'

build_graphs([('A', 'B', 4), ('B', 'B', 5), ('B', 'C', 9)])
insert_shortest_path_tests('A', 'C', ['A', 'B', 'C'], ['A', 'B', 'B', 'C'])
graphs_impossible_to_color.add(test)






colors = ['red', 'yellow', 'green', 'blue', 'purple', 'white']

coloring_algorithms = [
    color_graph_brute_force,
    color_graph_greedy,
]

for coloring_algorithm in coloring_algorithms:
    print '%s' % coloring_algorithm.__name__

    for test_name, graph_types in test_graphs.iteritems():
        print '\t%s' % test_name

        graph = graph_types['unweighted_undirected_colored']

        d = max([len(node.neighbors) for node in graph])
        d_plus_one_colors = colors[:d + 1]

        for node in graph:
            node.color = None

        coloring_algorithm(graph, d_plus_one_colors)

        expected_colored = True
        if test_name in graphs_impossible_to_color:
            expected_colored = False

        if is_graph_legally_colored(graph) != expected_colored:
            raise Exception('Not legally colored: %s' % test_name)
