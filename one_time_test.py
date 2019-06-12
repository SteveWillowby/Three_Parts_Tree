import networkx as nx
from full_approximate_rule_miner import *

G = nx.read_adjlist("graphs/dblp_cite.edge_list", nodetype=int)
G = nx.DiGraph(G)
for node in G.nodes():
    if node in G.neighbors(node):
        G.remove_edge(node, node)
        print("Hi %s" % node)


rm = FullApproximateRuleMiner(G, 2, 2)

while not rm.done():
    best_rule = rm.determine_best_rule()
    rm.contract_valid_tuples(best_rule)
rm.cost_comparison()
