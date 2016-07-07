import random
from collections import defaultdict

from coloring import Node, color_graph_brute_force, color_graph_greedy, is_graph_legally_colored
from weighted_directed_acyclic_graph import TopologicalOrderDfs, topological_order_kahns, shortest_path as topological_shortest_path
from weighted_directed_cyclic_graph import shortest_path_djikstras, shortest_path_djikstras_priority_queue
from unweighted_undirected_cyclic_graph import shortest_path_bfs


def build_weighted_directed_graph(nodes, edges):

    graph = {node: [] for node in nodes}

    for direct_predecessor, direct_successor, weight in edges:
        graph[direct_predecessor].append((direct_successor, weight))

    return graph


def build_unweighted_undirected_graph(nodes, edges):

    graph = {node: [] for node in nodes}

    for node_1, node_2, weight in edges:
        for node_a, node_b in ((node_1, node_2), (node_2, node_1)):
            edge_count = get_edge_count(node_a, node_b, edges)
            while graph[node_a].count(node_b) < edge_count:
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

            edge_count = get_edge_count(in_node.label, out_node.label, edges)
            while out_node.neighbors.count(in_node) < edge_count:
                out_node.neighbors.append(in_node)

    return graph


def get_edge_count(node_a, node_b, edges):
    a_b_count = 0
    b_a_count = 0
    for node_1, node_2, weight in edges:
        if (node_1, node_2) == (node_a, node_b):
            a_b_count += 1
        if (node_2, node_1) == (node_a, node_b):
            b_a_count += 1
    return max(a_b_count, b_a_count)


def build_graphs(edges, input_nodes=None):
    if input_nodes != None:
        graph_nodes = input_nodes
    else:
        graph_nodes = nodes

    for graph_type, build_graph_type in graph_types.iteritems():
        test_graphs[test][graph_type] = build_graph_type(graph_nodes, edges)


graph_types = {
    'weighted_directed':             build_weighted_directed_graph,
    'unweighted_undirected':         build_unweighted_undirected_graph,
    'unweighted_undirected_colored': build_unweighted_undirected_colored_graph,
}


test_graphs = defaultdict(dict)

shortest_paths = {}

directed_cyclic_graphs = set()

expected_failures = set()


nodes = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

test = None # test name


def add_shortest_path_tests(start_node, target_node, first_shortest_path, second_shortest_path):
    shortest_paths[test] = {
        1: (start_node, target_node, first_shortest_path),
        2: (start_node, target_node, second_shortest_path),
    }

def add_expected_failure(function_name, error_message):
    expected_failures.add((test, function_name, error_message))


test = 'empty graph'

build_graphs([], [])
add_shortest_path_tests('A', 'B', None, None)
add_expected_failure('topological_order_kahns', 'Start or target node not in graph')
add_expected_failure('TopologicalOrderDfs', 'Start or target node not in graph')
add_expected_failure('shortest_path_bfs', 'Start or target node not in graph')
add_expected_failure('shortest_path_djikstras', 'Start or target node not in graph')
add_expected_failure('shortest_path_djikstras_priority_queue', 'Start or target node not in graph')


test = 'one node'

build_graphs([], ['A'])
add_shortest_path_tests('A', 'B', None, None)
add_expected_failure('topological_order_kahns', 'Start or target node not in graph')
add_expected_failure('TopologicalOrderDfs', 'Start or target node not in graph')
add_expected_failure('shortest_path_bfs', 'Start or target node not in graph')
add_expected_failure('shortest_path_djikstras', 'Start or target node not in graph')
add_expected_failure('shortest_path_djikstras_priority_queue', 'Start or target node not in graph')


test = 'disconnected'

build_graphs([])
add_shortest_path_tests('A', 'D', None, None)


test = 'line'

build_graphs([('A', 'B', 6), ('B', 'C', 9), ('C', 'D', 4), ('D', 'E', 7), ('E', 'F', 4),
              ('F', 'G', 1)])
add_shortest_path_tests('D', 'G', ['D', 'E', 'F', 'G'], None)


test = 'leaf'

build_graphs([('A', 'B', 1), ('A', 'C', 4), ('B', 'D', 2), ('C', 'E', 3), ('D', 'F', 7),
              ('E', 'G', 1)])
add_shortest_path_tests('A', 'D', ['A', 'B', 'D'], None)


test = 'tree'

build_graphs([('A', 'B', 2), ('A', 'C', 9), ('B', 'D', 3), ('B', 'E', 1), ('C', 'F', 4),
              ('E', 'G', 2)])
add_shortest_path_tests('A', 'G', ['A', 'B', 'E', 'G'], None)


test = 'negative edges'

build_graphs([('A', 'B', -3), ('A', 'C', -1), ('B', 'D', -5), ('B', 'E', -4), ('C', 'F', -2),
              ('E', 'G', -6), ('F', 'E', -1)])
add_shortest_path_tests('A', 'G', ['A', 'B', 'E', 'G'], ['A', 'C', 'D', 'E', 'G'])


test = 'cycle'

build_graphs([('A', 'B', 6), ('B', 'C', 9), ('C', 'D', 4), ('D', 'E', 7), ('E', 'F', 4),
              ('F', 'G', 1), ('G', 'A', 9)])
add_shortest_path_tests('B', 'D', ['B', 'C', 'D'], None)
directed_cyclic_graphs.add(test)


test = 'cyclic'

build_graphs([('A', 'B', 1), ('A', 'C', 3), ('A', 'D', 7), ('B', 'C', 3), ('C', 'A', 9),
              ('D', 'E', 4), ('D', 'F', 5), ('E', 'F', 3), ('F', 'E', 2), ('F', 'G', 9)])
add_shortest_path_tests('A', 'F', ['A', 'D', 'F'], ['A', 'D', 'E', 'F'])
directed_cyclic_graphs.add(test)


test = 'negative cyclic'

build_graphs([('A', 'B', -1), ('A', 'C', -3), ('A', 'D', -7), ('B', 'C', -3), ('C', 'A', -9),
              ('D', 'E', -4), ('D', 'F', -9), ('E', 'F', -3), ('F', 'E', -2), ('F', 'G', -9)])
add_shortest_path_tests('A', 'F', ['A', 'D', 'F'], ['A', 'D', 'E', 'F'])
directed_cyclic_graphs.add(test)


test = 'loop'

build_graphs([('A', 'B', 4), ('B', 'B', 5), ('B', 'C', 9)])
add_shortest_path_tests('A', 'C', ['A', 'B', 'C'], ['A', 'B', 'B', 'C'])
directed_cyclic_graphs.add(test)
add_expected_failure('color_graph_brute_force', 'Legal coloring impossible')
add_expected_failure('color_graph_greedy', 'Legal coloring impossible for node with loop')


test = 'negative loop'

build_graphs([('A', 'B', 4), ('B', 'B', -3), ('B', 'C', 9)])
add_shortest_path_tests('A', 'C', ['A', 'B', 'C'], ['A', 'B', 'B', 'C'])
directed_cyclic_graphs.add(test)
add_expected_failure('color_graph_brute_force', 'Legal coloring impossible')
add_expected_failure('color_graph_greedy', 'Legal coloring impossible for node with loop')


test = 'complete/nonplanar'

edges = [('D', 'B', 1), ('D', 'C', 1), ('C', 'B', 1)]
for node in nodes:
    for neighbor in nodes:
        if (node != neighbor) and ((node, neighbor) not in [('D', 'B'), ('D', 'C'), ('C', 'B')]):
            edges.append((node, neighbor, random.randint(3, 9)))
build_graphs(edges)
add_shortest_path_tests('D', 'B', ['D', 'B'], ['D', 'C', 'B'])
directed_cyclic_graphs.add(test)


test = 'wheel center'

build_graphs([('A', 'B', 1), ('A', 'C', 4), ('A', 'D', 2), ('A', 'E', 6), ('A', 'F', 3),
              ('A', 'G', 3), ('B', 'C', 3), ('C', 'D', 3), ('D', 'E', 5), ('E', 'F', 8),
              ('F', 'G', 8), ('G', 'B', 2)])
add_shortest_path_tests('A', 'E', ['A', 'E'], ['A', 'D', 'E'])
directed_cyclic_graphs.add(test)


test = 'wheel outside'

build_graphs([('A', 'B', 1), ('A', 'C', 4), ('A', 'D', 2), ('A', 'E', 6), ('A', 'F', 3),
              ('A', 'G', 3), ('B', 'C', 3), ('C', 'D', 3), ('D', 'E', 5), ('E', 'F', 8),
              ('F', 'G', 8), ('G', 'B', 2)])
add_shortest_path_tests('F', 'G', ['F', 'G'], ['F', 'A', 'G'])
directed_cyclic_graphs.add(test)


test = 'star'

build_graphs([('A', 'B', 5), ('A', 'C', 6), ('A', 'D', 3), ('A', 'E', 7), ('A', 'F', 1),
              ('A', 'G', 2)])
add_shortest_path_tests('A', 'D', ['A', 'D'], None)


test = 'bipartite'

build_graphs([('A', 'F', 4), ('B', 'E', 2), ('B', 'G', 3), ('C', 'F', 6), ('C', 'G', 3),
              ('D', 'E', 3), ('D', 'G', 3), ('E', 'B', 3), ('G', 'C', 3), ('G', 'D', 3)])
add_shortest_path_tests('D', 'F', ['D', 'G', 'C', 'F'], ['D', 'E', 'B', 'G', 'C', 'F'])
directed_cyclic_graphs.add(test)


test = 'nodes vs weight'

build_graphs([('A', 'B', 6), ('A', 'C', 1), ('B', 'D', 9), ('C', 'E', 2), ('D', 'G', 7),
              ('E', 'F', 1), ('F', 'G', 1)])


test = 'no directed path'

build_graphs([('A', 'B', 6), ('B', 'C', 9), ('C', 'D', 4), ('D', 'E', 7), ('E', 'F', 4),
              ('F', 'G', 1)])


test = 'multiple edges'

build_graphs([('A', 'B', 4), ('A', 'C', 1), ('A', 'C', 5), ('B', 'D', 7), ('C', 'F', 7),
              ('F', 'G', 1), ('F', 'G', 4)])
add_shortest_path_tests('A', 'G', ['A', 'C', 'F', 'G'], ['A', 'C', 'F', 'G'])


test = 'a'

build_graphs([('A', 'B', 3), ('A', 'D', 2), ('B', 'A', 1), ('B', 'C', 2), ('B', 'D', 4),
              ('C', 'E', 5), ('C', 'F', 9), ('D', 'A', 2)],
             ['A', 'B', 'C', 'D', 'E', 'F'])
add_shortest_path_tests('B', 'A', ['B', 'A'], ['B', 'D', 'A'])
directed_cyclic_graphs.add(test)


test = 'b'

build_graphs([('A', 'B', 1), ('A', 'C', 4), ('A', 'F', 4), ('B', 'E', 9), ('D', 'C', 6),
              ('D', 'E', 8), ('D', 'F', 7), ('D', 'G', 4), ('F', 'C', 2), ('G', 'A', 1),
              ('G', 'E', 3)])
add_shortest_path_tests('A', 'C', ['A', 'C'], ['A', 'F', 'C'])


test = 'c'

build_graphs([('A', 'B', 1), ('A', 'C', 1), ('A', 'D', 1), ('B', 'A', 1), ('B', 'C', 1),
              ('C', 'A', 1), ('C', 'B', 1), ('C', 'E', 1), ('D', 'A', 1), ('D', 'F', 1),
              ('D', 'G', 1), ('E', 'C', 1), ('E', 'H', 1), ('F', 'D', 1), ('F', 'I', 1),
              ('G', 'D', 1), ('G', 'I', 1), ('H', 'E', 1), ('H', 'I', 1), ('I', 'F', 1),
              ('I', 'G', 1), ('I', 'H', 1)],
             ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'])
add_shortest_path_tests('A', 'G', ['A', 'D', 'G'], ['A', 'D', 'F', 'I', 'G'])
directed_cyclic_graphs.add(test)




results = defaultdict(int)

def pass_(cyclic=False):
    print 'ok' if not cyclic else 'ok (cyclic)'
    results['pass'] += 1

def fail(message, cyclic=False):
    if cyclic:
        message = '%s (cyclic)' % message
    print 'FAIL: %s' % message
    results['fail'] += 1

def get_expected_failure(test_name, algorithm):
    for failure in expected_failures:
        if (test_name, algorithm.__name__) == failure[0:2]:
            return failure
    return None

def verify_expected_failure(expected_failure, exception):
    if expected_failure and expected_failure[2] in exception.message:
        pass_()
    else:
        fail(exception.message)


# coloring

coloring_algorithms = [
    color_graph_brute_force,
    color_graph_greedy,
]

colors = ['red', 'yellow', 'green', 'blue', 'purple', 'white', 'orange', 'black']

for coloring_algorithm in coloring_algorithms:
    print '\n%s' % coloring_algorithm.__name__

    for test_name, graph_types in iter(sorted(test_graphs.iteritems())):
        print '\t%s' % test_name.ljust(20),

        graph = graph_types['unweighted_undirected_colored']

        try:
            d = max([len(node.neighbors) for node in graph])
        except ValueError:
            d = 0

        d_plus_one_colors = colors[:d + 1]

        for node in graph:
            node.color = None

        expected_failure = get_expected_failure(test_name, coloring_algorithm)

        try:
            coloring_algorithm(graph, d_plus_one_colors)
        except Exception as e:
            verify_expected_failure(expected_failure, e)
            continue
        else:
            if expected_failure:
                fail('Failed to raise error: %s' % expected_failure[2])
                continue

        if not is_graph_legally_colored(graph):
            fail('Not legally colored')
            continue

        pass_()


# weighted directed acyclic

test = 'nodes vs weight'
add_shortest_path_tests('A', 'G', ['A', 'C', 'E', 'F', 'G'], ['A', 'B', 'D', 'G'])

test = 'no directed path'
add_shortest_path_tests('C', 'A', None, None)

topological_ordering_algorithms = [
    TopologicalOrderDfs,
    topological_order_kahns,
]

def is_topologically_ordered(graph, topologically_ordered_nodes):
    for node, direct_successors in graph.iteritems():
        for direct_successor, edge_weight in direct_successors:
            try:
                if topologically_ordered_nodes.index(node) > topologically_ordered_nodes.index(direct_successor):
                    return False
            except ValueError:
                return False
    return True

for topological_ordering_algorithm in topological_ordering_algorithms:
    print '\n%s' % topological_ordering_algorithm.__name__

    for test_name, graph_types in iter(sorted(test_graphs.iteritems())):
        print '\t%s' % test_name.ljust(20),

        graph = graph_types['weighted_directed']

        start_node, target_node, shortest_path = shortest_paths[test_name][1]

        try:
            topologically_ordered_nodes = topological_ordering_algorithm(graph).order_graph()
        except AttributeError:
            topologically_ordered_nodes = topological_ordering_algorithm(graph)
        except RuntimeError:
            fail('RuntimeError', test_name in directed_cyclic_graphs)
            continue

        if not is_topologically_ordered(graph, topologically_ordered_nodes):
            fail('Not topologically sorted', test_name in directed_cyclic_graphs)
            continue

        expected_failure = get_expected_failure(test_name, topological_ordering_algorithm)

        try:
            if topological_shortest_path(graph, topologically_ordered_nodes, start_node, target_node) != shortest_path:
                fail('Not shortest path', test_name in directed_cyclic_graphs)
                continue
        except Exception as e:
            verify_expected_failure(expected_failure, e)
            continue
        else:
            if expected_failure:
                fail('Failed to raise error: %s' % expected_failure[2])
                continue

        pass_(cyclic=test_name in directed_cyclic_graphs)


# weighted directed cyclic

test = 'nodes vs weight'
add_shortest_path_tests('A', 'G', ['A', 'C', 'E', 'F', 'G'], ['A', 'B', 'D', 'G'])

test = 'no directed path'
add_shortest_path_tests('C', 'A', None, None)

djikstras_algorithms = [
    shortest_path_djikstras,
    shortest_path_djikstras_priority_queue,
]

for djikstras_algorithm in djikstras_algorithms:
    print '\n%s' % djikstras_algorithm.__name__

    for test_name, graph_types in iter(sorted(test_graphs.iteritems())):

        print '\t%s' % test_name.ljust(20),

        if 'negative' in test_name:
            print 'skipped'
            continue

        graph = graph_types['weighted_directed']

        start_node, target_node, shortest_path = shortest_paths[test_name][1]

        expected_failure = get_expected_failure(test_name, djikstras_algorithm)

        try:
            if djikstras_algorithm(graph, start_node, target_node) != shortest_path:
                fail('Not shortest path')
                continue
        except Exception as e:
            verify_expected_failure(expected_failure, e)
            continue
        else:
            if expected_failure:
                fail('Failed to raise error: %s' % expected_failure[2])
                continue

        pass_()


# unweighted undirected cyclic

test = 'nodes vs weight'
add_shortest_path_tests('A', 'G', ['A', 'B', 'D', 'G'], ['A', 'C', 'E', 'F', 'G'])

test = 'no directed path'
add_shortest_path_tests('C', 'A', ['C', 'B', 'A'], None)

print '\n%s' % 'shortest_path_bfs'

for test_name, graph_types in iter(sorted(test_graphs.iteritems())):
    print '\t%s' % test_name.ljust(20),

    graph = graph_types['unweighted_undirected']

    start_node, target_node, shortest_path = shortest_paths[test_name][1]

    expected_failure = get_expected_failure(test_name, shortest_path_bfs)

    try:
        if shortest_path_bfs(graph, start_node, target_node) != shortest_path:
            fail('Not shortest path')
            continue
    except Exception as e:
        verify_expected_failure(expected_failure, e)
        continue
    else:
        if expected_failure:
            fail('Failed to raise error: %s' % expected_failure[2])
            continue

    pass_()

print
for result in ['pass', 'fail']:
    print result.ljust(6), results[result]

print '\ndone\n'
