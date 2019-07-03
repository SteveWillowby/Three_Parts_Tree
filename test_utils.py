import networkx as nx
import random

def n_ary_tree(size, n):
    G=nx.DiGraph()
    for i in range(1, size + 1):
        G.add_node(i)
    for i in range(1, size + 1):
        for j in range(0, n):
            if i * n + j - (n - 2) < size + 1:
                G.add_edge(i, i * n + j - (n - 2))
    return G

def n_ary_tree_of_k_rings(size, n, k):
    tree_size = int(size / k)
    leftovers = size % k

    G = nx.DiGraph()
    for i in range(1, size):
        G.add_node(i)
    # Make the rings:
    for tree_idx in range(1, tree_size + 1):
        graph_idx = (tree_idx - 1) * k + 1
        for ring_idx in range(graph_idx, graph_idx + k - 1):
            G.add_edge(ring_idx, ring_idx + 1)
        G.add_edge(graph_idx + k - 1, graph_idx)
    # Make the tree:
    for tree_idx in range(1, tree_size + 1):
        graph_idx = (tree_idx - 1) * k + 1
        ring_bottom = graph_idx + int(k / 2)
        for j in range(0, n):
            next_tree_idx = tree_idx * n + j - (n - 2)
            next_graph_idx = (next_tree_idx - 1) * k + 1
            if next_graph_idx <= tree_size * k:
                G.add_edge(ring_bottom, next_graph_idx)
    return G

# Note that, due to the current coding, and rewiring_prob over 0.5 will cause all edges to be rewired.
def watts_strogatz(size, k, bidirected=True):
    G = nx.DiGraph()
    for i in range(0, size):
        G.add_node(i)
    for i in range(0, size):
        for j in range(1, k + 1):
            G.add_edge(i, (i + j) % size)
            if bidirected:
                G.add_edge((i + j) % size, i)
    return G

def rewire_graph(G, rewiring_prob):
    original_edges = set([edge for edge in G.edges()])
    rewired_edges = set()
    # Choose which edges to rewire and delete them from the graph.
    for edge in original_edges:
        if random.uniform(0.0, 0.999999999999999) < rewiring_prob:
            rewired_edges.add(edge)
            G.remove_edge(edge[0], edge[1])
    
    # Put the rewired edges back into the graph.
    final_edges = original_edges - rewired_edges
    nodes = list(G.nodes())
    for edge in rewired_edges:
        new_edge = (nodes[random.randint(0, len(nodes) - 1)], nodes[random.randint(0, len(nodes) - 1)])
        while new_edge in final_edges: # While there's a collision
            new_edge = (nodes[random.randint(0, len(nodes) - 1)], nodes[random.randint(0, len(nodes) - 1)])
        G.add_edge(new_edge[0], new_edge[1])
        final_edges.add(new_edge)

def remove_self_loops(G):
    for node in G.nodes():
        if (node, node) in G.edges():
            G.remove_edge(node, node)
