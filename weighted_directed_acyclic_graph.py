from itertools import islice


class TopologicalOrderDfs:

    def __init__(self, graph):
        self.graph = graph

    def order_graph(self):

        self.reverse_topologically_ordered_nodes = []
        self.visited_nodes = set()

        for node in self.graph:
            if node not in self.visited_nodes:
                self.order_node_dfs(node)

        return list(reversed(self.reverse_topologically_ordered_nodes))

    def order_node_dfs(self, node):

        for direct_successor, edge_weight in self.graph[node]:
            if direct_successor not in self.visited_nodes:
                self.order_node_dfs(direct_successor)

        self.reverse_topologically_ordered_nodes.append(node)
        self.visited_nodes.add(node)


def topological_order_kahns(graph):

    topologically_ordered_nodes = []

    node_to_number_of_incoming_edges = {
        node: 0 for node in graph
    }

    for node, direct_successors in graph.iteritems():
        for direct_successor, edge_weight in direct_successors:
            node_to_number_of_incoming_edges[direct_successor] += 1

    nodes_with_no_incoming_edges = set(
        [node for node, number_of_incoming_edges in node_to_number_of_incoming_edges.iteritems()
         if number_of_incoming_edges == 0]
    )

    while len(nodes_with_no_incoming_edges):

        node_with_no_incoming_edges = nodes_with_no_incoming_edges.pop()

        topologically_ordered_nodes.append(node_with_no_incoming_edges)

        for node, direct_successors in graph[node_with_no_incoming_edges]:
            node_to_number_of_incoming_edges[node] -= 1
            if node_to_number_of_incoming_edges[node] == 0:
                nodes_with_no_incoming_edges.add(node)

    return topologically_ordered_nodes


def shortest_path(graph, topologically_ordered_nodes, start_node, target_node):

    shortest_path_values       = {start_node: 0}
    shortest_path_predecessors = {}

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


# notes:
#
# Dijkstra's, Bellman-Ford, A*
# negative cycles
# disconnected graphs


# tests

def is_topologically_ordered(graph, topologically_ordered_nodes):
    for node, direct_successors in graph.iteritems():
        for direct_successor, edge_weight in direct_successors:
            if topologically_ordered_nodes.index(node) > topologically_ordered_nodes.index(direct_successor):
                return False
    return True


graph_tests = [
    ({
        'A': [('B', 2), ('C', 4)],
        'B': [('D', 1), ('E', 6)],
        'C': [('E', 9), ('F', 3)],
        'D': [],
        'E': [('D', 7)],
        'F': [],
    },
    'A', 'E', ['A', 'B', 'E']),

    ({
        'G': [('H', 1), ('I', 1), ('L', 1)],
        'H': [('K', 1)],
        'I': [],
        'J': [('I', 1), ('K', 1), ('L', 1), ('M', 1)],
        'K': [],
        'L': [('I', 1)],
        'M': [('G', 1), ('K', 1)],
    },
    'G', 'I', ['G', 'I']),
]

topological_ordering_algorithms = [
    TopologicalOrderDfs,
    topological_order_kahns,
]

for graph, start_node, target_node, expected_shortest_path in graph_tests:

    for topological_ordering_algorithm in topological_ordering_algorithms:

        try:
            topologically_ordered_nodes = topological_ordering_algorithm(graph).order_graph()
        except AttributeError:
            topologically_ordered_nodes = topological_ordering_algorithm(graph)

        if not is_topologically_ordered(graph, topologically_ordered_nodes):
            raise Exception('Not topologically ordered')

    if shortest_path(graph, topologically_ordered_nodes, start_node, target_node) != expected_shortest_path:
        raise Exception('Not shortest path')
