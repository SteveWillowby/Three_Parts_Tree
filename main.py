import networkx as nx
from networkx import utils
from simple_rule_miner import *
from approximate_rule_miner import *

G=nx.DiGraph()

size = 7

# Builds a binary tree:
for i in range(1, size + 1):
    G.add_node(i)
for i in range(1, size + 1):
    if i * 2 < size + 1:
        G.add_edge(i, i*2)
    if i * 2 + 1 < size + 1:
        G.add_edge(i, i*2 + 1)

rm = ApproximateRuleMiner(G)

print("\nFor binary tree:")
while not rm.done():
    best_rule = rm.determine_best_rule()
    rm.contract_valid_tuples(best_rule)

G = nx.DiGraph(nx.random_k_out_graph(size, 2, 0.2))
print(G.edges())
rm = ApproximateRuleMiner(G)

print("\nFor random k out 2, 0.2:")
while not rm.done():
    best_rule = rm.determine_best_rule()
    rm.contract_valid_tuples(best_rule)

G = nx.DiGraph(nx.barabasi_albert_graph(size, 2))
rm = ApproximateRuleMiner(G)

print("\nFor Barabasi Albert:")
while not rm.done():
    best_rule = rm.determine_best_rule()
    rm.contract_valid_tuples(best_rule)
