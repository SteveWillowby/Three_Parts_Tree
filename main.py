import networkx as nx
from networkx import utils
from simple_rule_miner import *

G=nx.scale_free_graph(100)

rm = SimpleRuleMiner(G)
