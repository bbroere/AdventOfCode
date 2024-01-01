import networkx


# Thanks to reddit and hyper-neutrino (https://github.com/hyper-neutrino) for introducing me to networkx, this would
# have saved me so much time during my master thesis
def part_1(filename: str) -> int:
    lines = open(filename).read().splitlines()
    # we are going to construct a graph
    graph = networkx.Graph()
    # add all edges
    for line in lines:
        node, children = line.split(': ')
        for child in children.split(' '):
            graph.add_edge(node, child)
    # check that the graph is connected
    assert networkx.is_connected(graph)
    # now we determine the minimum cut (https://en.wikipedia.org/wiki/Minimum_cut) of the graph, which is a set of nodes
    # we assume that this problem has a unique solution, as it is an aoc problem of course
    min_cut = networkx.minimum_edge_cut(graph)
    # so we check the min cut has length 3, as in we need to cut 3 edges
    assert len(min_cut) == 3
    # now remove the edges in the cut from the graph
    graph.remove_edges_from(min_cut)
    # and we check the graph is no longer connected and split in 2 parts
    assert len(list(networkx.connected_components(graph))) == 2
    # so get the parts and multiply their node sizes
    p1, p2 = networkx.connected_components(graph)
    return len(p1) * len(p2)
