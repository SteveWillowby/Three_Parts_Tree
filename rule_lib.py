import networkx as nx
from networkx import utils
from networkx.algorithms import isomorphism
from utils import *

class RuleLib:
    """Stores grammar rules in order of how frequently they've been found"""

    def __init__(self):
        self._rules = {}
        self._next_id = 0

    # Give an id number for a rule. Check existing ones first in order of frequency.
    # Runtime of this is O(|rules|*isomorphism_check)
    def add_rule(self, graph):
        size = len(graph.nodes())
        if size not in self._rules:
            self._rules[size] = [[graph, self._next_id, 1]]
            self._next_id += 1
            return self._next_id - 1
        else:
            rules = self._rules[size]
            for i in range(0, len(rules)):
                gm = isomorphism.DiGraphMatcher(rules[i][0], graph)
                if gm.is_isomorphic():
                    # Note that this rule appeared once more.
                    rules[i][2] += 1
                    # Move the rule closer to the front of the list if it's more popular.
                    j = i - 1
                    while j >= 0 and rules[j][2] < rules[i][2]:
                        j -= 1
                    j += 1
                    if i != j and rules[j][2] < rules[i][2]:
                        temp = rules[j]
                        rules[j] = rules[i]
                        rules[i] = temp
                        return rules[j][1]
                    return rules[i][1]
            # If not already in the library.
            rules[size].append([graph, self._next_id, 1])
            self._next_id += 1
            return self._next_id - 1
