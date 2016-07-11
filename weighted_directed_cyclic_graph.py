# find the shortest path from a start node to a target node in
# a weighted, directed, cyclic graph with no negative edges


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
# from the start node, calculate the distance to each direct successor. then go the direct
# successor with the shortest distance and calculate the shortest distance so far to each
# of its direct successors. repeat for every node, always choosing the node with the
# shortest distance as the next node
#
# time:   O(N^2)   where N is the number of nodes. for every node, we go through all the
#                  unvisited nodes (N * the summation 1..N). we also iterate over all
#                  the edges M, but drop that linear cost on the edges because of the
#                  quadratic cost on the nodes
# space:  O(N)     the unvisited nodes set holds all the nodes, and in the worst case
#                  the shortest path dictionaries and list hold all the nodes

def shortest_path_djikstras(graph, start_node, target_node):

    if (start_node not in graph) or (target_node not in graph):
        raise Exception('Start or target node not in graph')

    # to track the shortest path to each node, initialize dictionaries
    # to hold the path's distance and previous node
    shortest_path_distances = {node: float('inf') for node in graph}
    shortest_path_distances[start_node] = 0
    shortest_path_direct_predecessors = {}

    unvisited_nodes = set(graph)

    while len(unvisited_nodes):

        # get the unvisited node with the shortest distance
        current_node = None
        min_distance = float('inf')
        for node in unvisited_nodes:
            if shortest_path_distances[node] <= min_distance:
                current_node = node
                min_distance = shortest_path_distances[node]

        # stop when we reach the target node
        if current_node == target_node:
            break

        for direct_successor, edge_weight in graph[current_node]:

            # get the shortest distance we have to the direct successor so far
            # and the distance to the direct successor from the current node
            shortest_distance_so_far   = shortest_path_distances[direct_successor]
            distance_from_current_node = shortest_path_distances[current_node] + edge_weight

            if distance_from_current_node < shortest_distance_so_far:

                # update the direct successor's shortest path
                shortest_path_distances[direct_successor] = distance_from_current_node
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


# Dijkstra's algorithm (priority queue)
#
# to find the node with the shortest distance so far, use a priority queue with the distance
# as the key instead of iterating over all the unvisited nodes and greedily finding the node
# with the shortest distance
#
# time:   O((N+M)logN)   where N is the number of nodes and M is the number of edges. popping
#                        from the heap takes logN time, and we pop N times. pushing to the
#                        heap takes logN time, and in the worst case all M edge weights give
#                        shorter distances to a node. heapifying the graph, checking for the
#                        start and target node in the graph, and building the shortest path
#                        all take N time, but N is a less significant term than NlogN
# space:  O(N+M)         in the worst case the visitied nodes set, the shortest path list, and
#                        the shortest path dictionaries hold all the nodes. and the heap holds
#                        (distance, node) pairs for all M edge weights

import heapq

def shortest_path_djikstras_priority_queue(graph, start_node, target_node):

    if (start_node not in graph) or (target_node not in graph):
        raise Exception('Start or target node not in graph')

    # to track the shortest path to each node, initialize dictionaries
    # to hold the path's distance and previous node
    shortest_path_distances = {node: float('inf') for node in graph}
    shortest_path_distances[start_node] = 0
    shortest_path_direct_predecessors = {}

    # set up a priority queue (binary heap) of the nodes
    # with the distance to the node as the key
    priority_queue = [(shortest_path_distances[node], node) for node in graph]
    heapq.heapify(priority_queue)

    # when we find a shorter distance to a node, we'll add the node to the heap
    # again with the new distance instead of updating the distance in the heap
    # (becauase with the built in heapq, updating or deleting entries takes O(N)
    # not O(logN) time) so we'll track the nodes we visit to avoid visiting
    # nodes again at outdated longer distances
    visited_nodes = set()

    while len(priority_queue):

        current_node_distance, current_node = heapq.heappop(priority_queue)

        if current_node in visited_nodes:
            continue

        # stop when we reach the target node
        if current_node == target_node:
            break

        for direct_successor, edge_weight in graph[current_node]:

            # get the shortest distance we have to the direct successor so far
            # and the distance to the direct successor from the current node
            shortest_distance_so_far   = shortest_path_distances[direct_successor]
            distance_from_current_node = shortest_path_distances[current_node] + edge_weight

            if distance_from_current_node < shortest_distance_so_far:

                # update the direct successor's shortest path
                shortest_path_distances[direct_successor] = distance_from_current_node
                shortest_path_direct_predecessors[direct_successor] = current_node

                # add the new distance to the priority queue
                heapq.heappush(priority_queue, (distance_from_current_node, direct_successor))

        visited_nodes.add(current_node)

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
# implementing heap for O(logN) decrease_key and O(N) space
# fibonacci heap
# insert nodes in priority queue as they're discovered
#
# negative cycles (Bellman-Ford)
# considering A*
# reverse list (or insert at beginning) operations
# expressing M in terms of N (complete)
# expressing N in terms of M (connected)
#
# edge cases
#     less than 2 nodes in graph
#     start node and target node are the same
#     start node or target node aren't in graph
#     loop
#     multiple edges
#     invalid graph (negative edges)
#     no path (disconnected or wrong directions)
#     only 1 path (no second shortest path)
#     start or target node in cycle
