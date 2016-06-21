# find the second shortest path from a start node to a
# target node in a weighted, directed, acyclic graph


# nodes are represented by a dictionary of (string, list) pairs where the string
# is the node value and the list holds tuples of the node's direct successors
# (string, int) where the string is the direct successor's value and the int is
# the weight of the edge to the direct successor

graph = {
    'A': [('B', 7)],
    'B': [('A', 3), ('C', 9)],
    'C': [],
}


# topological ordering overview

# if we can order the nodes so every node comes after all its predecessors, we can iterate
# over the nodes in one pass from the start node to the target node and track the shortest
# path so far to each node's direct successors. this ordering is possible because the
# graph is directed and acyclic


# topological ordering (dfs)
#
# using dfs visit each node and add the node to the ordering when it has no successors or all
# its successors have been added. all edges must point to a node earlier in the ordering
#
# time:   O(N+M)   where N is the number of nodes and M is the number of edges. we go through
#                  every node and its outgoing edges
# space:  O(N)     the ordered nodes always take up N space and the call stack uses N space
#                  in the worst case (graph is a straight line from start to target node)

class TopologicalOrderDfs:

    def __init__(self, graph):
        self.graph = graph

    def order_graph(self):

        # initialize a list to hold the ordered nodes and a
        # set to track which nodes we've already added
        self.reverse_topologically_ordered_nodes = []
        self.added_nodes = set()

        # the first node might not be a predecessor of all the other
        # nodes or the graph might be disconnected, so we need to
        # iterate over all the nodes
        for node in self.graph:
            if node not in self.added_nodes:
                self.order_node_dfs(node)

        return list(reversed(self.reverse_topologically_ordered_nodes))

    def order_node_dfs(self, node):

        # recursively visit direct successors
        for direct_successor, edge_weight in self.graph[node]:
            if direct_successor not in self.added_nodes:
                self.order_node_dfs(direct_successor)

        # add a node when it has no direct successors or all
        # its successors have been added
        self.reverse_topologically_ordered_nodes.append(node)
        self.added_nodes.add(node)


# topological ordering (Khan's algorithm)
#
# keep adding nodes to the ordering that have no predecessors or whose predecessors have all
# been added. all edges must point to a node later in the ordering
#
# time:   O(N+M)   where N is the number of nodes and M is the number of edges. we go through
#                  every node and its outgoing edges
# space:  O(N)     the output and dictionary holding the numbers of incoming edges use N space
#                  and the set of nodes with no incoming edges uses N space in the worst case

def topological_order_kahns(graph):

    topologically_ordered_nodes = []

    # initialize a dictionary to track the number of incoming edges to
    # each node from nodes that haven't been added to the ordering yet
    node_to_number_of_incoming_edges = {
        node: 0 for node in graph
    }

    for node, direct_successors in graph.iteritems():
        for direct_successor, edge_weight in direct_successors:
            node_to_number_of_incoming_edges[direct_successor] += 1

    # find all the nodes with no incoming edges
    nodes_with_no_incoming_edges = set(
        [node for node, number_of_incoming_edges in node_to_number_of_incoming_edges.iteritems()
         if number_of_incoming_edges == 0]
    )

    while len(nodes_with_no_incoming_edges):

        node_with_no_incoming_edges = nodes_with_no_incoming_edges.pop()

        topologically_ordered_nodes.append(node_with_no_incoming_edges)

        # since we added the node, decrement the number of incoming edges for
        # all the node's direct successors
        for direct_successor, edge_weight in graph[node_with_no_incoming_edges]:
            node_to_number_of_incoming_edges[direct_successor] -= 1

            # check if that was the direct successor's last incoming edge
            if node_to_number_of_incoming_edges[direct_successor] == 0:
                nodes_with_no_incoming_edges.add(direct_successor)

    return topologically_ordered_nodes


# shortest path
#
# traverse the topologically ordered nodes from the start node to the target node
# checking to see if a node can give a shorter path to its direct successors
#
# time:   O(N+M)   where N is the number of nodes and M is the number of edges. in the worst
#                  case the start node is the first node and the target node is the last
#                  node so we go through all the nodes and their direct successors
# space:  O(N)     the output, shortest path values, and shortest path predecessors hold all
#                  the nodes in the worst case

from itertools import islice

def shortest_path(graph, topologically_ordered_nodes, start_node, target_node):

    # to track the shortest path to each node, initialize dictionaries
    # to hold the path's distance and previous node
    shortest_path_distances    = {start_node: 0}
    shortest_path_predecessors = {start_node: None}

    try:
        start_node_index  = topologically_ordered_nodes.index(start_node)
        target_node_index = topologically_ordered_nodes.index(target_node)
    except ValueError:
        raise Exception('Start or target node not in graph')

    # traverse the topologically ordered nodes from the start node to the target node
    for current_node in islice(topologically_ordered_nodes, start_node_index, target_node_index):

        for direct_successor, edge_weight in graph[current_node]:

            # get the shortest distance to the current node and to the direct successor
            # or an arbitrarily large value if we haven't found a path yet
            current_node_shortest_path_value     = shortest_path_distances.get(current_node, float('inf'))
            direct_successor_shortest_path_value = shortest_path_distances.get(direct_successor, float('inf'))

            # if the current node's path to the direct successor is the shortest
            # path so far, update the direct successor's shortest path
            if current_node_shortest_path_value + edge_weight < direct_successor_shortest_path_value:
                shortest_path_distances[direct_successor]    = current_node_shortest_path_value + edge_weight
                shortest_path_predecessors[direct_successor] = current_node

    # if the target node doesn't have a previous node, there's no shortest path
    if not shortest_path_predecessors.get(target_node):
        return []

    # backtrack the shortest path
    reverse_shortest_path = []
    current_node = target_node

    while current_node:
        reverse_shortest_path.append(current_node)
        current_node = shortest_path_predecessors.get(current_node)

    return list(reversed(reverse_shortest_path))


# notes:
#
# considering Dijkstra's, Bellman-Ford, A*
# negative cycles
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
