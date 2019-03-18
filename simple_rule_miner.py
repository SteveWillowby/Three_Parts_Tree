import networkx as nx
from networkx import utils
from rule_miner_base import *
from rule import *
from rule_lib import *

class SimpleRuleMiner(RuleMinerBase):
    """Used to find and compress grammar rules in a graph"""

    def __init__(self, G):
        self._G = G
        self._rule_findings = {}

    def determine_best_rule(self):
        nodes = list(self._G.nodes())
        rule_lib = RuleLib()
        not_a_real_rule = Rule([0,1],self._G)
        found_a_rule = -1
        for i in range(2, len(nodes)):
            indices = [j for j in range(0, i)]
            done = False
            while not done:
                t = [nodes[idx] for idx in indices]
                if self.is_tuple_valid(t):
                    rule_lib.add_rule(not_a_real_rule._rule_graph(t, self._G))
                    found_a_rule = i

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
            if found_a_rule > -1:
                break
        print(f"The best rule is a graph with edges {rule_lib._rules[found_a_rule + 2][0][0].edges()} occuring {rule_lib._rules[found_a_rule + 2][0][2]} times")


    def is_tuple_valid(self, t):
        ins = {}
        outs = {}
        counters = {}
        for n in t:
            counters[n] = 0
        max_in_len = 0
        max_out_len = 0
        for n in t:
            ins[n] = [edge[0] for edge in self._G.in_edges(n) if edge[0] not in counters]
            ins[n].sort()
            if len(ins[n]) > 0 and len(ins[n]) != max_in_len:
                if max_in_len != 0:
                    return False
                max_in_len = len(ins[n])
            outs[n] = [edge[1] for edge in self._G.out_edges(n) if edge[1] not in counters]
            outs[n].sort()
            if len(outs[n]) > 0 and len(outs[n]) != max_out_len:
                if max_out_len != 0:
                    return False
                max_out_len = len(outs[n])
        done_count = 0
        while done_count < len(t):
            done_count = 0
            first_iter = True
            for n in t:
                if len(ins[n]) == 0:
                    done_count += 1
                    continue
                if counters[n] >= len(ins[n]):
                    done_count += 1
                    curr_finished = True
                else:
                    curr_finished = False
                    curr_node = ins[n][counters[n]]
                if not first_iter:
                    if curr_finished != prev_finished or curr_node != prev_node:
                        # print(f"Tuple {t} fails on in edges -- {curr_finished} {prev_finished} {curr_node} {prev_node}")
                        return False
                first_iter = False
                prev_finished = curr_finished
                prev_node = curr_node

                counters[n] += 1

        for n in t:
            counters[n] = 0
        done_count = 0
        while done_count < len(t):
            done_count = 0
            first_iter = True
            for n in t:
                if len(outs[n]) == 0:
                    done_count += 1
                    continue
                if counters[n] >= len(outs[n]):
                    done_count += 1
                    curr_finished = True
                else:
                    curr_finished = False
                    curr_node = outs[n][counters[n]]
                if not first_iter:
                    if curr_finished != prev_finished or curr_node != prev_node:
                        # print(f"Tuple {t} fails on out edges")
                        return False
                first_iter = False
                prev_finished = curr_finished
                prev_node = curr_node
                counters[n] += 1
        return True



    def contract_valid_tuples(self, rule):
        pass