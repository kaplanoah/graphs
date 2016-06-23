# legally color an unweighted, undirected graph using
# D+1 or fewer colors where D is the maximum degree


# nodes are represented by a list of node objects that have a label,
# a list of neighbors (an adjacency list), and a color

class Node:

    def __init__(self, label):
        self.label = label
        self.neighbors = []
        self.color = None


# brute force
#
# try every possible combination of colors until we find a legal coloring
#
# time:   O(C^N * N+M)   where C is the number of colors, N is the number of nodes, and M is the
#                        number of edges. for every combination of colors, we check if the
#                        coloring is legal by going through every node once and every edge twice
# space:  O(1)           itertools.product is an iterator

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

            # ensure neighbors have different colors
            if (node.color == neighbor.color) or (not node.color):
                return False

    return True


# greedy
#
# with ordered nodes and colors, go through each node and color it with the first
# available legal color
#
# time:   O(N+M)   where N is the number of nodes and M is the number of edges. we go
#                  through every node once and every edge twice
# space:  O(D)     we need to track all the illegal colors for each node

def color_graph_greedy(graph, colors):

    for node in graph:

        if node in node.neighbors:
            raise Exception('Legal coloring impossible for node with loop: %s' % node.label)

        # get all the node's neighbors' colors
        illegal_colors = set([neighbor.color for neighbor in node.neighbors if neighbor.color])

        # assign the first legal color
        node.color = [color for color in colors if color not in illegal_colors][0]


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
# expressing C and M in terms of N
# backtracking (not needed because we know D+1 colors work)
#
# edge cases
#     loop
