import networkx as nx
from networkx import utils
from rule_miner_base import *

class SimpleRuleMiner(RuleMinerBase):
    """Used to find and compress grammar rules in a graph"""

    def __init__(self, G):
        self._G = G
        self._rule_findings = {}

    def determine_best_rule(self):
        nodes = self._G.nodes()
        for i in range(2, len(nodes)):
            indices = [j for j in range(0, i)]
            done = False
            while not done:
                

                indices_idx = i - 1
                indices[indices_idx] += 1
                while indices[indices_idx] == len(nodes) - (i - indices_idx) + 1:
                    indices[indices_idx] = -1 # Note that the loop finished.
                    if indices_idx == 0:
                        done = True
                        break
                    indices_idx -= 1
                    indices[indices_idx] += 1
                if not done:
                    while indices_idx < i:
                        if indices[indices_idx] == -1:
                            indices[indices_idx] = indices[indices_idx - 1] + 1
                        indices_idx += 1

    def contract_valid_tuples(self, rule):
        pass