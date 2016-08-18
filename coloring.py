# legally color an unweighted, undirected graph using
# D+1 or fewer colors where D is the maximum degree


# graphs are represented by a list of node objects that have a label,
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
# time:   O(D^N * N+M)   where N is the number of nodes and M is the number of edges. for every
#                        combination of colors, we check if the coloring is legal by going
#                        through every node once and every edge twice
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

# time:   O(ND+M)   where N is the number of nodes and M is the number of edges. we go
#                   through every color for every node, and every edge from each end
#                   twice to check if it's a loop and to get the illegal colors for
#                   the node at the other end
# space:  O(D)      we store all the illegal and legal colors for every node

def color_graph_greedy_d(graph, colors):

    for node in graph:

        if node in node.neighbors:
            raise Exception('Legal coloring impossible for node with loop: %s' % node.label)

        # get the node's neighbors' colors, as a set so we
        # can check if a color is illegal in constant time
        illegal_colors = set([neighbor.color for neighbor in node.neighbors if neighbor.color])

        # assign the first legal color
        node.color = [color for color in colors if color not in illegal_colors][0]


# time:   O(N+M)   where N is the number of nodes and M is the number of edges. we go
#                  through every node once, every edge from each end twice to check
#                  if it's a loop and to get the illegal colors for the node at the
#                  other end, and the colors twice up to at most one more color than
#                  the number of edges
# space:  O(D)     we store all the illegal colors for each node, which will be D if
#                  the neighbors of the node with the maximum degree all have
#                  different colors

def color_graph_greedy(graph, colors):

    for node in graph:

        if node in node.neighbors:
            raise Exception('Legal coloring impossible for node with loop: %s' % node.label)

        # get the node's neighbors' colors, as a set so we
        # can check if a color is illegal in constant time
        illegal_colors = set([neighbor.color for neighbor in node.neighbors if neighbor.color])

        # assign the first legal color. by using a generator expression we
        # don't store all the legal colors and we iterate over at most one
        # more color than the number of illegal colors
        node.color = next(color for color in colors if color not in illegal_colors)


# time:   O(NM^2)   where N is the number of nodes and M is the number of edges. we go
#                   through every node once, and every edge twice for every color up
#                   to at most one more color than the number of illegal colors
# space:  O(1)      we use generators so we don't store any colors

def color_graph_greedy_constant_space(graph, colors):

    for node in graph:

        if node in node.neighbors:
            raise Exception('Legal coloring impossible for node with loop: %s' % node.label)

        # assign the first legal color. by using generator expressions we don't
        # don't store colors, but we iterate over every neighbor for every
        # color up to at most one more color than the number of neighbors
        node.color = next(color for color in colors if color not in
            (neighbor.color for neighbor in node.neighbors if neighbor.color)
        )


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
# set of colors (unordered)
# itertools by hand
# temporarily destructive (risky with multithreating)
# expressing D and M in terms of N
# backtracking (not needed because we know D+1 colors work)
#
# edge cases
#     loop
