import networkx as nx
from networkx import utils
from simple_rule_miner import *
from approximate_rule_miner import *
import heapq
from bitstring import BitArray

b = BitArray(length=0)
b.append(1)
print(b.bin)
b.clear()
print(b.bin)
b.append(BitArray(length=3, uint=1))
print(b.bin)

new_heap = []
heapq.heappush(new_heap, 7)
heapq.heappush(new_heap, 3)
heapq.heappush(new_heap, 11)
heapq.heappush(new_heap, 15)
heapq.heappush(new_heap, 2)
heapq.heappush(new_heap, 12)
heapq.heappush(new_heap, 7)
print(new_heap)
print([heapq.heappop(new_heap) for i in range(0, 7)])
print(new_heap)

G=nx.DiGraph()

size = 1024

# Builds a binary tree:
for i in range(1, size + 1):
    G.add_node(i)
for i in range(1, size + 1):
    if i * 2 < size + 1:
        G.add_edge(i, i*2)
    if i * 2 + 1 < size + 1:
        G.add_edge(i, i*2 + 1)

rm = ApproximateRuleMiner(G)

print("\nFor binary tree with %s nodes:" % size)
while not rm.done():
    best_rule = rm.determine_best_rule()
    rm.contract_valid_tuples(best_rule)


# Tree of rings:

ring_size = 4
tree_size = int(size / ring_size)
leftovers = size % ring_size

G = nx.DiGraph()
for i in range(1, size):
    G.add_node(i)
for tree_idx in range(1, tree_size + 1):
    # Make the ring.
    graph_idx = (tree_idx - 1) * ring_size + 1
    for ring_idx in range(graph_idx, graph_idx + ring_size - 1):
        G.add_edge(ring_idx, ring_idx + 1)
    G.add_edge(graph_idx + ring_size - 1, graph_idx)
    # Add pointers to the other rings.
    ring_bottom = graph_idx + int(ring_size / 2)
    next_graph_idx = ((tree_idx * 2) - 1) * ring_size + 1
    if next_graph_idx <= tree_size * ring_size:
        G.add_edge(ring_bottom, next_graph_idx)
    next_graph_idx = ((tree_idx * 2 + 1) - 1) * ring_size + 1
    if next_graph_idx <= tree_size * ring_size:
        G.add_edge(ring_bottom, next_graph_idx)

rm = ApproximateRuleMiner(G)

print("\nFor tree of size-%s rings with %s nodes:" % (ring_size, size))
while not rm.done():
    best_rule = rm.determine_best_rule()
    rm.contract_valid_tuples(best_rule)

# Directed double-ring:

G = nx.DiGraph()
for i in range(1, size + 1):
    G.add_node(i)
for i in range(1, size):
    G.add_edge(i, i + 1)
    G.add_edge(i + 1, i)
G.add_edge(1, size)
G.add_edge(size, 1)

rm = ApproximateRuleMiner(G)

print("\nFor directed double-ring of size: %s" % size)
while not rm.done():
    best_rule = rm.determine_best_rule()
    rm.contract_valid_tuples(best_rule)

"""
# Directed erdosh reyni:
expected_num_edges = size * 2
prob_of_edge_numerator = expected_num_edges
prob_of_edge_denominator = size * (size - 1)  # No div by 2 since we multiply by 2 because we can have bidirected edges.
G = nx.DiGraph()
for i in range(1, size + 1):
    G.add_node(i)
for i in range(1, size + 1):
    for j in range(1, size + 1):
        if j == i:
            continue
        if random.randint(1, prob_of_edge_denominator) <= prob_of_edge_numerator:
            G.add_edge(i, j)

rm = ApproximateRuleMiner(G)

print("\nFor directed erdosh-reyni with %s nodes and %s edges:" % (size, len(G.edges())))
while not rm.done():
    best_rule = rm.determine_best_rule()
    rm.contract_valid_tuples(best_rule)
"""
