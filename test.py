import networkx as nx
import sys
from full_approximate_rule_miner import *
from test_utils import *

graph_size = int(sys.argv[1])
min_rule = int(sys.argv[2])
max_rule = int(sys.argv[3])
test_type = sys.argv[4]
graph_type = sys.argv[5]

G = None
if graph_type == "n_tree":
    n = int(sys.argv[6])
    G = n_ary_tree(graph_size, n) 
elif graph_type == "n_tree_of_k_rings":
    n = int(sys.argv[6])
    k = int(sys.argv[7])
    G = n_ary_tree_of_k_rings(size, n, k)
elif graph_type == "watts_strogatz":
    n = int(sys.argv[6])
    rewiring_prob = 0
    if len(sys.argv) > 7:
        rewiring_prob = float(sys.argv[7])
    bidirected = 0
    if len(sys.argv) > 8:
        bidirected = int(sys.argv[8])
    G = watts_strogatz(graph_size, n, rewiring_prob, bidirected)
else:
    print("Unknown graph type %s" % graph_type)
    exit(1)

rm = FullApproximateRuleMiner(G, min_rule, max_rule)

while not rm.done():
    best_rule = rm.determine_best_rule()
    rm.contract_valid_tuples(best_rule)
rm.cost_comparison()
