import networkx as nx
from networkx import utils
from simple_rule_miner import *

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

rm = SimpleRuleMiner(G)

while len(G.nodes()) > 1:
    best_rule = rm.determine_best_rule()
    print(f"Rule id: {best_rule[0].id()} Occurrences: {best_rule[1:len(best_rule)]}")
    rm.contract_valid_tuples(best_rule)
