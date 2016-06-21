# find the second shortest path from a start node to a target
# node in a weighted, directed, acyclic graph


# nodes are represented by a dictionary of (string, list) pairs where the string
# is the node value and the list holds tuples of the node's direct successors
# (string, int) where the string is the direct successor's value and the int is
# the weight of the edge to the direct successor

graph = {
    'A': [('B', 7)],
    'B': [('A', 3), ('C', 9)],
    'C': [],
}


# shortest path using topological ordering

# by ordering the nodes so that every node comes after all its predecessors, we can
# iterate over the nodes and find the shortest path to each node. this ordering is possible
# because the graph is directed and acyclic


# topological ordering (dfs)
#
# visit each node using dfs and add the node to the ordering when it has no successors or
# no unvisited successors. so all edges must point to a node that's already been added
#
# time:   O(N+M)   where N is the number of nodes and M is the number of edges. we go through
#                  every node and its outgoing edges
# space:  O(N)     the ordered nodes always take up N space and the call stack uses N space
#                  in the worst case (graph is a straight line from start to target node)

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


# topological ordering (Khan's algorithm)
#
# keep adding nodes to the ordering that have no successors or no successors that haven't
# already been added
#
# time:   O(N+M)   where N is the number of nodes and M is the number of edges. we go through
#                  every node and its outgoing edges
# space:  O(N)     the output and dictionary holding the numbers of incoming edges use N space
#                  and the set of nodes with no incoming edges uses N space in the worst case

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


# shortest path
#
# use topologically sorted nodes
#
# time:   O(N+M)   where N is the number of nodes and M is the number of edges. in the worst
#                  case the start node is the first node and the target node is the last
#                  node so we go through all the nodes and their direct successors
# space:  O(N)     the output, shortest path values, and shortest path predecessors hold all
#                  the nodes in the worst case

from itertools import islice

def shortest_path(graph, topologically_ordered_nodes, start_node, target_node):

    shortest_path_values       = {start_node: 0}
    shortest_path_predecessors = {}

    try:
        start_node_index  = topologically_ordered_nodes.index(start_node)
        target_node_index = topologically_ordered_nodes.index(target_node)
    except ValueError:
        raise Exception('Start or target node not in graph')

    for current_node in islice(topologically_ordered_nodes, start_node_index, target_node_index):

        for direct_successor, edge_weight in graph[current_node]:

            current_node_shortest_path_value     = shortest_path_values.get(current_node, float('inf'))
            direct_successor_shortest_path_value = shortest_path_values.get(direct_successor, float('inf'))

            if current_node_shortest_path_value + edge_weight < direct_successor_shortest_path_value:
                shortest_path_values[direct_successor]       = current_node_shortest_path_value + edge_weight
                shortest_path_predecessors[direct_successor] = current_node

    if not shortest_path_predecessors.get(target_node):
        return []

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
