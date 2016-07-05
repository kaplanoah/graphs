# find the shortest path from a start node to a
# target node in a weighted, directed, cyclic graph


# graphs are represented by a dictionary of (string, list) pairs where the string
# is the node value and the list holds tuples of the node's direct successors
# (string, int) where the string is the direct successor's value and the int is
# the weight of the edge to the direct successor

graph = {
    'A': [('B', 7)],
    'B': [('A', 3), ('C', 9)],
    'C': [],
}


# Dijkstra's algorithm
#
# keep adding nodes to the ordering that have no predecessors or whose predecessors have all
#
# time:   O(N+M)   where N is the number of nodes and M is the number of edges. we go through
#                  every node and its outgoing edges
# space:  O(N)     the output and dictionary holding the numbers of incoming edges use N space
#                  and the set of nodes with no incoming edges uses N space in the worst case

def shortest_path_djikstras(graph, start_node, target_node):

    unvisited_nodes = set()

    shortest_path_distances    = {}
    shortest_path_predecessors = {}

    for node in graph:
        shortest_path_distances[node]    = float('inf')
        shortest_path_predecessors[node] = None
        unvisited_nodes.add(node)

    shortest_path_distances[start_node]    = 0
    shortest_path_predecessors[start_node] = None

    while len(unvisited_nodes):

        min_distance = float('inf')
        for node in unvisited_nodes:
            if shortest_path_distances[node] <= min_distance:
                min_distance = shortest_path_distances[node]
                current_node = node

        unvisited_nodes.remove(current_node)

        for direct_successor, edge_weight in graph[current_node]:

            current_node_shortest_path_value = shortest_path_distances[current_node]
            direct_successor_shortest_path_value = shortest_path_distances[direct_successor]

            if current_node_shortest_path_value + edge_weight < direct_successor_shortest_path_value:
                shortest_path_distances[direct_successor]    = current_node_shortest_path_value + edge_weight
                shortest_path_predecessors[direct_successor] = current_node

    # if the target node doesn't have a previous node, there's no shortest path
    if not shortest_path_predecessors.get(target_node):
        return None

    # backtrack the shortest path
    reverse_shortest_path = []
    current_node = target_node

    while current_node:
        reverse_shortest_path.append(current_node)
        current_node = shortest_path_predecessors.get(current_node)

    return list(reversed(reverse_shortest_path))



# notes:
#
# considering Bellman-Ford (negative cycles), A*
# reverse list (or insert at beginning) operations
# expressing M in terms of N
#
# edge cases
#     less than 2 nodes in graph
#     start node and target node are the same
#     start node or target node aren't in graph
#     invalid graph (cyclic, loop)
#     negative edges
#     multiple edges
#     no path (disconnected or wrong directions)
#     only 1 path (no second shortest path)
#     start or target node in cycle
