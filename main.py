import networkx as nx
from networkx import utils
from simple_rule_miner import *
from approximate_rule_miner import *

G=nx.DiGraph()

size = 40

# Builds a binary tree:
for i in range(0, size):
    G.add_node(i)
for i in range(0, size):
    if i * 2 < size:
        G.add_edge(i, i*2)
    if i * 2 + 1 < size:
        G.add_edge(i, i*2 + 1)

rm = ApproximateRuleMiner(G)

print("\nFor binary tree:")
while not rm.done():
    best_rule = rm.determine_best_rule()
    print(f"Rule id: {best_rule[0]} Projected Occurrences: {best_rule[1]}")
    rm.contract_valid_tuples(best_rule)

G = nx.DiGraph(nx.random_k_out_graph(size, 2, 0.2))
print(G.edges())
rm = ApproximateRuleMiner(G)

print("\nFor random k out 2, 0.2:")
while not rm.done():
    best_rule = rm.determine_best_rule()
    print(f"Rule id: {best_rule[0]} Projected Occurrences: {best_rule[1]}")
    rm.contract_valid_tuples(best_rule)

G = nx.DiGraph(nx.barabasi_albert_graph(size, 2))
rm = ApproximateRuleMiner(G)

print("\nFor Barabasi Albert:")
while not rm.done():
    best_rule = rm.determine_best_rule()
    print(f"Rule id: {best_rule[0]} Projected Occurrences: {best_rule[1]}")
    rm.contract_valid_tuples(best_rule)
