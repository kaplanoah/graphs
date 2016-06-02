from Queue import Queue


def shortest_path_bfs(graph, start_node, target_node):

    visited_nodes = set()
    queue = Queue()

    visited_nodes.add(start_node)
    queue.put(start_node)

    shortest_path_distances      = {start_node: 0}
    shortest_path_previous_nodes = {}

    while not queue.empty():
        node = queue.get()

        for neighbor in graph[node]:
            if neighbor not in visited_nodes:

                shortest_path_distances[neighbor] = shortest_path_distances[node] + 1
                shortest_path_previous_nodes[neighbor] = node

                queue.put(neighbor)
                visited_nodes.add(neighbor)

    reverse_shortest_path = []
    current_node = target_node

    while current_node:
        reverse_shortest_path.append(current_node)
        current_node = shortest_path_previous_nodes.get(current_node)

    return list(reversed(reverse_shortest_path))


def test():

    graph_tests = [
        ({
            'A': ['B', 'C'],
            'B': ['A', 'D', 'E'],
            'C': ['A', 'F'],
            'D': ['B', 'E'],
            'E': ['B', 'D'],
            'F': ['C'],
        },
        'A', 'E', ['A', 'B', 'E']),

        ({
            'G': ['H', 'I', 'J'],
            'H': ['G', 'I'],
            'I': ['G', 'H', 'K'],
            'J': ['G', 'L', 'M'],
            'K': ['I', 'N'],
            'L': ['J', 'O'],
            'M': ['J', 'O'],
            'N': ['K', 'O'],
            'O': ['L', 'M', 'N'],
        },
        'G', 'N', ['G', 'I', 'K', 'N']),
    ]

    for graph, start_node, target_node, expected_shortest_path in graph_tests:
        for _ in xrange(10000):

            if shortest_path_bfs(graph, start_node, target_node) != expected_shortest_path:
                raise Exception('Not shortest path')

test()
