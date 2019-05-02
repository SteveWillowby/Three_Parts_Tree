import networkx as nx
from networkx import utils
from simple_rule_miner import *
from approximate_rule_miner import *

G=nx.DiGraph()

size = 1023

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

G = nx.DiGraph(nx.barabasi_albert_graph(size, 2))
rm = ApproximateRuleMiner(G)

print("\nFor Barabasi Albert:")
while not rm.done():
    best_rule = rm.determine_best_rule()
    rm.contract_valid_tuples(best_rule)
