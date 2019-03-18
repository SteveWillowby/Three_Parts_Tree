import networkx as nx
from networkx import utils
from simple_rule_miner import *

G=nx.DiGraph()
G.add_node(0)
G.add_node(1)
G.add_node(2)
G.add_node(3)
G.add_node(4)
G.add_node(5)

G.add_edge(0,1)
G.add_edge(1,2)
G.add_edge(2,3)
G.add_edge(3,4)
G.add_edge(4,5)
G.add_edge(5,0)

rm = SimpleRuleMiner(G)

rm.determine_best_rule()
