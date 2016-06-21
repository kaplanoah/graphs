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
# using bfs visit each node and store the distance to the node and the previous node in
# the path we took. because the graph is unweighted and we're using bfs, the first time
# we visit a node we know we've used the shortest path to get to that node
#
# time:   O(N+M)   where N is the number of nodes and M is the number of edges. we go through
#                  every node once and check every edge twice
# space:  O(N)     where N is the number of nodes. if the graph isn't disconnected, the set of
#                  visited nodes and dictionaries for the shortest path hold all the nodes

from Queue import Queue

def shortest_path_bfs(graph, start_node, target_node):

    if start_node not in graph or target_node not in graph:
        raise Exception('Start or target node not in graph')

    # initialize a queue of nodes whose neighbors we need to visit
    # and a set to track nodes we've already visited
    queue = Queue()
    visited_nodes = set()

    # queue and visit the start node
    queue.put(start_node)
    visited_nodes.add(start_node)

    # initialize dictionaries to track the distance of the shortest
    # path to each node and that path's previous node
    shortest_path_distances      = {start_node: 0}
    shortest_path_previous_nodes = {}

    while not queue.empty():

        # visit each node's unvisited neighbors
        node = queue.get()
        for neighbor in graph[node]:
            if neighbor not in visited_nodes:

                # set the shortest path distance and previous node
                shortest_path_distances[neighbor] = shortest_path_distances[node] + 1
                shortest_path_previous_nodes[neighbor] = node

                # queue the neighbor to visit it's neighbors
                queue.put(neighbor)
                visited_nodes.add(neighbor)

    # if the target node doesn't have a previous node, there's no shortest path
    if not shortest_path_previous_nodes.get(target_node):
        return []

    # backtrack the shortest path
    reverse_shortest_path = []
    current_node = target_node

    while current_node:
        reverse_shortest_path.append(current_node)
        current_node = shortest_path_previous_nodes.get(current_node)

    return list(reversed(reverse_shortest_path))


# notes:
#
# considering Dijkstra's, Bellman-Ford, A*
# reverse list (or insert at beginning) operations
# expressing M in terms of N
# O(B^D) runtime
#
# edge cases
#     less than 2 nodes in graph
#     start node and target node are the same
#     start node or target node aren't in graph
#     multiple edges, loops
#     no path (disconnected)
#     only 1 path (no second shortest path)
