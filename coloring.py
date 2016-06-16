# legally color an unweighted, undirected graph using
# D+1 or fewer colors, where D is the maximum degree


# nodes are represented by a list of node objects that have a label,
# a list of neighbors, and a color (effectively an adjacency list)

class Node:

    def __init__(self, label):
        self.label = label
        self.neighbors = []
        self.color = None


# brute force
#
# try every possible combination of colors until we find a legal coloring
#
# time:   O(C^N * N+M)  where C is the number of colors and N is the number of nodes. this is
#                       effectively O(N^N) in a graph where one node connects to all other nodes
#                       because D would be N-1 and C is defined as D+1
#                       except for multiple edges
# space:  O(1)          itertools.product is an iterator

import itertools

def color_graph_brute_force(graph, colors):

    # get the cartesian product of all the colors, for every node
    # (every color for every color, for as many nodes as we need to color)
    for current_coloring in itertools.product(colors, repeat=len(graph)):

        # assign current coloring to all nodes
        for index, node in enumerate(graph):
            node.color = current_coloring[index]

        if is_graph_legally_colored(graph):
            return

    if not is_graph_legally_colored(graph):
        raise Exception('Legal coloring impossible')


def is_graph_legally_colored(graph):

    for node in graph:
        for neighbor in node.neighbors:
            if (node.color == neighbor.color) or (not node.color):
                return False
    return True


# greedy
#
# with ordered nodes and colors, color each node with the first color that's legal
#
# time:   O(N+M)  where N is the number of nodes and M is the number of edges.
#                 but M is triangular series of N-1 in a complete graph (every node
#                 connected) so can be O(N^2). M is useful because it more closely
#                 gives the big o for all graphs, not just complete graphs
# space:  O(D)    we need to track the illegal colors for a node, which is at most
#                 all of the colors except 1, or the maximum degree, which in the
#                 worse case in N-1

def color_graph_greedy(graph, colors):

    for node in graph:

        if node in node.neighbors:
            raise Exception('Legal coloring impossible for node with loop: %s' % node.label)

        illegal_colors = set([neighbor.color for neighbor in node.neighbors if neighbor.color])

        for color in colors:
            if color not in illegal_colors:
                node.color = color
                break


# notes:
#
# might want an even ratio of colors
# might want as few colors as possible (NP-complete)
#
# order matters in greedy coloring
# can order nodes to color based on
#     high degree
#     number of colored neighbors
#     high saturation (most unique neighbor colors)
#
# backtracking (not needed because we know D+1 colors work)
#
# edge cases
#     loop
