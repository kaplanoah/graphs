# find the second shortest path from a start node to a target
# node in an unweighted, undirected, cyclic graph


# nodes are represented by a dictionary of (string, list) pairs where the string
# is the node value and the list holds the node's neighbors' values

graph = {
    'A': ['B'],
    'B': ['A', 'C'],
    'C': ['B'],
}


# breadth first search
#
# try every possible combination of colors until we find a legal coloring
#
# time:   O(N + M)  where N is the number of nodes and M is the number of edges. we go through every
#                   node once and check every edge twice (from the node at each end). can also be
#                   O(B^D) where B is the branching factor and D is the depth of the target node (if
#                   the graph is large, maybe infinitely large, and N and M aren't useful)
# space:  O(N)      the shortest path and the set of visited nodes hold all the nodes in the worst
#                   case (graph is a straight line)

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

    if not shortest_path_previous_nodes.get(target_node):
        return []

    reverse_shortest_path = []
    current_node = target_node

    while current_node:
        reverse_shortest_path.append(current_node)
        current_node = shortest_path_previous_nodes.get(current_node)

    return list(reversed(reverse_shortest_path))


# notes:
#
# Dijkstra's, Bellman-Ford, A*
# negative cycles
# disconnected graphs
# reverse list (or insert at beginning) operations
# O(B^D) runtime
# edge cases:
#     less than 2 nodes in graph
#     start node and target node are the same
#     start node or target node aren't in graph
#     multiple edges, loops
#     no path (disconnected)
#     only 1 path (no second shortest path)
