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

    if (start_node not in graph) or (target_node not in graph):
        raise Exception('Start or target node not in graph')

    unvisited_nodes = set(graph)

    # to track the shortest path to each node, initialize dictionaries
    # to hold the path's distance and previous node
    shortest_path_distances = {node: float('inf') for node in graph}
    shortest_path_distances[start_node] = 0
    shortest_path_direct_predecessors = {}

    while len(unvisited_nodes):

        # get the unvisited node with the shortest distance
        current_node = None
        min_distance = float('inf')
        for node in unvisited_nodes:
            if shortest_path_distances[node] <= min_distance:
                current_node = node
                min_distance = shortest_path_distances[node]

        # we can stop when we reach the target node
        if current_node == target_node:
            break

        for direct_successor, edge_weight in graph[current_node]:

            # get the shortest distance we have so far for the direct successor
            # and the distance from the current node to the direct successor
            shortest_path_so_far            = shortest_path_distances[direct_successor]
            shortest_path_from_current_node = shortest_path_distances[current_node] + edge_weight

            # if the current node's path to the direct successor is the shortest
            # path so far, update the direct successor's shortest path
            if shortest_path_from_current_node < shortest_path_so_far:
                shortest_path_distances[direct_successor] = shortest_path_from_current_node
                shortest_path_direct_predecessors[direct_successor] = current_node

        unvisited_nodes.remove(current_node)

    # if the target node doesn't have a previous node, there's no shortest path
    if not shortest_path_direct_predecessors.get(target_node):
        return None

    # backtrack the shortest path
    reverse_shortest_path = []
    current_node = target_node

    while current_node:
        reverse_shortest_path.append(current_node)
        current_node = shortest_path_direct_predecessors.get(current_node)

    return list(reversed(reverse_shortest_path))



# notes:
#
# negative cycles (Bellman-Ford)
# considering A*
# reverse list (or insert at beginning) operations
# expressing M in terms of N
#
# edge cases
#     less than 2 nodes in graph
#     start node and target node are the same
#     start node or target node aren't in graph
#     loop
#     negative edges
#     multiple edges
#     no path (disconnected or wrong directions)
#     only 1 path (no second shortest path)
#     start or target node in cycle
