from itertools import islice


graph_a = {
    'A': [('B', 2), ('C', 4)],
    'B': [('D', 1), ('E', 6)],
    'C': [('E', 9), ('F', 3)],
    'D': [],
    'E': [('D', 7)],
    'F': [],
}

graph_b = {
    'G': [('H', 1), ('I', 1), ('L', 1)],
    'H': [('K', 1)],
    'I': [],
    'J': [('I', 1), ('K', 1), ('L', 1), ('M', 1)],
    'K': [],
    'L': [('I', 1)],
    'M': [('G', 1), ('K', 1)],
}


def topological_order(graph):

    reverse_topologically_ordered_nodes = []

    visited_nodes = set()

    def dfs(node):
        for direct_successor, edge_weight in graph[node]:
            if direct_successor not in visited_nodes:
                dfs(direct_successor)
        reverse_topologically_ordered_nodes.append(node)
        visited_nodes.add(node)

    for node in graph:
        if node not in visited_nodes:
            dfs(node)

    return list(reversed(reverse_topologically_ordered_nodes))


def shortest_path(graph, topologically_ordered_nodes, start_node, target_node):

    shortest_path_values       = {start_node: 0}
    shortest_path_predecessors = {start_node: None}

    start_node_index = topologically_ordered_nodes.index(start_node)

    for current_node in islice(topologically_ordered_nodes, start_node_index, None):

        for direct_successor, edge_weight in graph[current_node]:

            current_node_shortest_path_value     = shortest_path_values.get(current_node, float('inf'))
            direct_successor_shortest_path_value = shortest_path_values.get(direct_successor, float('inf'))

            if current_node_shortest_path_value + edge_weight < direct_successor_shortest_path_value:
                shortest_path_values[direct_successor]       = current_node_shortest_path_value + edge_weight
                shortest_path_predecessors[direct_successor] = current_node

    reverse_shortest_path = []
    current_node = target_node

    while current_node:
        reverse_shortest_path.append(current_node)
        current_node = shortest_path_predecessors.get(current_node)

    return list(reversed(reverse_shortest_path))


def is_topologically_ordered(graph, topologically_ordered_nodes):
    for node, direct_successors in graph.iteritems():
        for direct_successor, edge_weight in direct_successors:
            if topologically_ordered_nodes.index(node) > topologically_ordered_nodes.index(direct_successor):
                return False
    return True


graph_tests = [
    (graph_a, 'A', 'E', ['A', 'B', 'E']),
    (graph_b, 'G', 'I', ['G', 'I']),
]


def test_graphs():

    for graph, start_node, target_node, expected_shortest_path in graph_tests:

        for _ in xrange(10000):

            topologically_ordered_nodes = topological_order(graph)

            if not is_topologically_ordered(graph, topologically_ordered_nodes):
                print 'NOT TOPOLOGICALLY ORDERED'
                break

            if shortest_path(graph, topologically_ordered_nodes, start_node, target_node) != expected_shortest_path:
                print 'NOT SHORTEST PATH'
                break

test_graphs()
