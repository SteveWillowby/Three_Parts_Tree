import networkx as nx
from full_approximate_rule_miner import *

G = nx.DiGraph()
# Min size at which k_min = 3 compresses better than k_min = 2 is 9 nodes.
# Min size at which (2, 3) compresses using 3-node rules is 17 nodes.
# Still uses 3-node rules with an edge deletion in the 17 node graph.
size = 9
for i in range(0, size):
    G.add_node(i)
    for j in range(0, i):
        G.add_edge(j, i)

edge_loss_pos = 0
#G.remove_edge(size - (3 + edge_loss_pos), size - (1 + edge_loss_pos))

rm = FullApproximateRuleMiner(G, 2, 3, 0)

while not rm.done():
    best_rule = rm.determine_best_rule()
    rm.contract_valid_tuples(best_rule)
rm.cost_comparison()
