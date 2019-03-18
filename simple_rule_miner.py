import networkx as nx
from networkx import utils
from rule_miner_base import *

class SimpleRuleMiner(RuleMinerBase):
    """Used to find and compress grammar rules in a graph"""

    def __init__(self, G):
        self._G = G

    def determine_best_rule(self):
        pass

    def contract_valid_tuples(self, rule):
        pass