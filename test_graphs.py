
class Node:

    def __init__(self, label):
        self.label = label
        self.neighbors = []
        self.color = None


def build_weighted_directed_graph(nodes, edges):

    graph = {node: [] for node in nodes}

    for predecessor, successor, weight in edges:
        graph[predecessor].append((successor, weight))

    return graph


def build_unweighted_undirected_graph(nodes, edges):

    graph = {node: [] for node in nodes}

    for node_a, node_b in edges:
        graph[node_a].append(node_b)
        graph[node_b].append(node_a)

    return graph


def build_unweighted_undirected_colored_graph(labels, edges):

    graph = [Node(label) for label in labels]

    for labels in edges:
        for node in graph:
            if node.label in labels:
                neighbor = labels[0] if labels[0] != node.label else labels[1]
                node.neighbors.append(neighbor)

    return graph


graph_types = {
    'weighted_directed':             build_weighted_directed_graph,
    'unweighted_undirected':         build_unweighted_undirected_graph,
    'unweighted_undirected_colored': build_unweighted_undirected_colored_graph,
}


test_graphs = {graph_type: {} for graph_type in graph_types}


def build_graphs(test_name, nodes, edges):
    for graph_type, build_graph_type in graph_types.iteritems():
        test_graphs[graph_type][test_name] = build_graph_type(nodes, edges)


# disconnected

nodes = ['A', 'B', 'C', 'D', 'E']
build_graphs('disconnected', nodes, [])
