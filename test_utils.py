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
def watts_strogatz(size, k, rewiring_prob=0, bidirected=True):
    G = nx.DiGraph()
    for i in range(0, size):
        G.add_node(i)
    for i in range(0, size):
        for j in range(1, k + 1):
            G.add_edge(i, (i + j) % size)
            if bidirected:
                G.add_edge((i + j) % size, i)

    if rewiring_prob > 0:
        max_value = int(1.0 / rewiring_prob)
        current_edges = list(G.edges())
        for edge in current_edges:
            if bidirected and edge[0] > edge[1]:
                continue
            if random.randint(1, max_value) == 1:
                # Randomly pick a new place for edge[0] to point
                new_target = edge[0]
                while new_target == edge[0] or (edge[0], new_target) in G.out_edges(edge[0]):
                    new_target = random.randint(0, size - 1)
                G.add_edge(edge[0], new_target)
                if bidirected:
                    G.add_edge(new_target, edge[0])

                G.remove_edge(edge[0], edge[1])
                if bidirected:
                    G.remove_edge(edge[1], edge[0])
    return G
