import networkx as nx
from networkx import utils
from rule_miner_base import *
from rule import *
from rule_lib import *
from sets import Set
from itertools import combinations
from itertools import chain
import random
# from collections import OrderedDict

class ApproximateRuleMiner(RuleMinerBase):
    """Used to find and compress grammar rules in a graph"""

    def __init__(self, G):
        self._G = G
        self.first_round = True

        self.in_sets = {}
        self.out_sets = {}
        # self.both_sets = {}
        for node in list(self._G.nodes()):
            in_set = Set([edge[0] for edge in self._G.in_edges(node)])
            out_set = Set([edge[1] for edge in self._G.out_edges(node)])
            # both_set = in_set | out_set
            # in_only_set = in_set - both_set
            # out_only_set = out_set - both_set
            self.in_sets[node] = in_set# OrderedDict(sorted(in_only_set))
            self.out_sets[node] = out_set# OrderedDict(sorted(out_only_set))
            # self.both_sets[node] = both_set # OrderedDict(sorted(both_set))

        self.rule_occurrences_by_pair = {}
        self.rule_occurrences_by_id = {}

    def check_all_pairs_for_rules(self):
        nodes = list(self._G.nodes())
        nodes.sort()
        for i in range(0, len(nodes)):
            node_a = nodes[i]
            self.rule_occurrences_by_pair[node_a] = {}
            for j in range(i + 1, len(nodes)):
                node_b = nodes[j]
                best_options_without_ids = self.best_options_for_pair(node_a, node_b)
                unique_best_options_with_ids = self.add_rule_ids_and_filter(best_options_without_ids)
                self.rule_occurrences_by_pair[node_a][node_b] = unique_best_options_with_ids
                for id_num, option in best_options_with_ids.items():
                    if id_num not in self.rule_occurrences_by_id:
                        self.rule_occurrences_by_id[id_num] = Set()
                    self.rule_occurrences_by_id[id_num].add((node_a, node_b))

    def check_pairs_containing_ids(self, ids):
        pass

    def determine_best_rule(self):
        nodes = list(self._G.nodes())
        rule_lib = RuleLib()
        rule_occurrences = {}
        for i in range(2, len(nodes) + 1):
            indices = [j for j in range(0, i)]
            done = False
            while not done:
                t = [nodes[idx] for idx in indices]
                if self.is_tuple_valid(t):
                    rule = Rule(t, self._G, rule_lib)
                    if rule.id() not in rule_occurrences:
                        rule_occurrences[rule.id()] = [{node: 1 for node in t}, rule, t]
                    else:
                        all_new_nodes = True
                        for node in t:
                            if node in rule_occurrences[rule.id()][0]:
                                all_new_nodes = False
                                break
                        if all_new_nodes:
                            for node in t:
                                rule_occurrences[rule.id()][0][node] = 1
                            rule_occurrences[rule.id()].append(t)
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
            if len(rule_occurrences) > 0:
                break
            else:
                print(f"Going to size {i + 1}")
        max_len = 0
        best_rule = []
        for rule, occurrences in rule_occurrences.items():
            if len(occurrences) > max_len:
                max_len = len(occurrences)
                best_rule = occurrences
        return best_rule[1:len(best_rule)]

    # Thanks to Mark Rushakoff on Stack Overflow for the basis of this function. Although I might not use it.
    """
    def powerset(self, iterable):
        "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
        s = list(iterable)
        return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))
    """

    def random_subset(self, iterable):
        subset = []
        for entity in entities:
            if random.randint(0,1):
                subset.append[entity]
        return subset

    # Returns all valid, cheapest ways to edit the pair.
    # Or, if the pair is already valid, returns an empty array.
    # Note that this may currently return duplicates.
    def best_options_for_pair(self, a, b):
        just_a = Set([a])
        just_b = Set([b])

        in_sets = [self.in_sets[a] - just_b, self.in_sets[b] - just_a]
        in_sets.append(in_sets[0] & in_sets[1])
        out_sets = [self.out_sets[a] - just_b, self.out_sets[b] - just_a]
        out_sets.append(out_sets[0] & out_sets[1])

        three_in_values = [len(in_sets[0]), len(in_sets[1]), len(in_sets[0]) + len(in_sets[1]) - 2 * len(in_sets[2])]
        three_out_values = [len(out_sets[0]), len(out_sets[1]), len(out_sets[0]) + len(out_sets[1]) - 2 * len(out_sets[2])]

        in_min = min(three_in_values)
        out_min = min(three_out_values)

        if in_min == 0 and out_min == 0:
            # Already valid! No modifications needed. TODO: Add ID
            return [[Set() for i in range(0,8)]]

        return_values = []

        # Distinct possible best edit options:
        if three_in_values[0] == in_min:
            if three_out_values[0] == out_min:
                # Delete a_in and delete a_out
                a_in_add = Set()
                a_in_del = in_sets[0]
                b_in_add = Set()
                b_in_del = Set()

                a_out_add = Set()
                a_out_del = out_sets[0]
                b_out_add = Set()
                b_out_del = Set()
                return_values.append([a_in_add, a_in_del, b_in_add, b_in_del, a_out_add, a_out_del, b_out_add, b_out_del])
            if three_out_values[1] == out_min:
                # Delete a_in and delete b_out
                a_in_add = Set()
                a_in_del = in_sets[0]
                b_in_add = Set()
                b_in_del = Set()

                a_out_add = Set()
                a_out_del = Set()
                b_out_add = Set()
                b_out_del = out_sets[1]
                return_values.append([a_in_add, a_in_del, b_in_add, b_in_del, a_out_add, a_out_del, b_out_add, b_out_del])
            if three_out_values[2] == out_min:
                # Delete a_in and move outs to intersection
                # There are actually 2^(out_sets[2]) ways to do this!

                a_only = out_sets[2] - out_sets[0]
                b_only = out_sets[2] - out_sets[1]
                a_only_subset = Set(random_subset(a_only)) # a will delete this
                b_only_subset = Set(random_subset(b_only)) # b will delete this

                a_in_add = Set()
                a_in_del = in_sets[0]
                b_in_add = Set()
                b_in_del = Set()

                a_out_add = b_only - b_only_subset # a adds what b does not delete
                a_out_del = a_only_subset
                b_out_add = a_only - a_only_subset # b adds what a does not delete
                b_out_del = b_only_subset
                return_values.append([a_in_add, a_in_del, b_in_add, b_in_del, a_out_add, a_out_del, b_out_add, b_out_del])
        if three_in_values[1] == in_min:
            if three_out_values[0] == out_min:
                # Delete b_in and delete a_out
                a_in_add = Set()
                a_in_del = Set()
                b_in_add = Set()
                b_in_del = in_sets[1]

                a_out_add = Set()
                a_out_del = in_sets[0]
                b_out_add = Set()
                b_out_del = Set()
                return_values.append([a_in_add, a_in_del, b_in_add, b_in_del, a_out_add, a_out_del, b_out_add, b_out_del])
            if three_out_values[1] == out_min:
                # Delete b_in and delete b_out
                a_in_add = Set()
                a_in_del = Set()
                b_in_add = Set()
                b_in_del = in_sets[1]

                a_out_add = Set()
                a_out_del = Set()
                b_out_add = Set()
                b_out_del = out_sets[1]
                return_values.append([a_in_add, a_in_del, b_in_add, b_in_del, a_out_add, a_out_del, b_out_add, b_out_del])
            if three_out_values[2] == out_min:
                # Delete b_in and move outs to intersection
                # There are actually 2^(out_sets[2]) ways to do this!

                a_only = out_sets[2] - out_sets[0]
                b_only = out_sets[2] - out_sets[1]
                a_only_subset = Set(random_subset(a_only)) # a will delete this
                b_only_subset = Set(random_subset(b_only)) # b will delete this

                a_in_add = Set()
                a_in_del = Set()
                b_in_add = Set()
                b_in_del = in_sets[1]

                a_out_add = b_only - b_only_subset # a adds what b does not delete
                a_out_del = a_only_subset
                b_out_add = a_only - a_only_subset # b adds what a does not delete
                b_out_del = b_only_subset
                return_values.append([a_in_add, a_in_del, b_in_add, b_in_del, a_out_add, a_out_del, b_out_add, b_out_del])
        if three_in_values[2] == in_min:
            if three_out_values[0] == out_min:
                # Move ins to intersection and delete a_out
                # There are actually 2^(in_sets[2]) ways to do this!

                a_only = in_sets[2] - in_sets[0]
                b_only = in_sets[2] - in_sets[1]
                a_only_subset = Set(random_subset(a_only)) # a will delete this
                b_only_subset = Set(random_subset(b_only)) # b will delete this

                a_in_add = b_only - b_only_subset # a adds what b does not delete
                a_in_del = a_only_subset
                b_in_add = a_only - a_only_subset # b adds what a does not delete
                b_in_del = b_only_subset
                
                a_out_add = Set()
                a_out_del = out_sets[0]
                b_out_add = Set()
                b_out_del = Set()
                return_values.append([a_in_add, a_in_del, b_in_add, b_in_del, a_out_add, a_out_del, b_out_add, b_out_del])
            if three_out_values[1] == out_min:
                # Move ins to intersection and delete b_out
                # There are actually 2^(in_sets[2]) ways to do this!

                a_only = in_sets[2] - in_sets[0]
                b_only = in_sets[2] - in_sets[1]
                a_only_subset = Set(random_subset(a_only)) # a will delete this
                b_only_subset = Set(random_subset(b_only)) # b will delete this

                a_in_add = b_only - b_only_subset # a adds what b does not delete
                a_in_del = a_only_subset
                b_in_add = a_only - a_only_subset # b adds what a does not delete
                b_in_del = b_only_subset

                a_out_add = Set()
                a_out_del = Set()
                b_out_add = Set()
                b_out_del = out_sets[1]
                return_values.append([a_in_add, a_in_del, b_in_add, b_in_del, a_out_add, a_out_del, b_out_add, b_out_del])
            if three_out_values[2] == out_min:
                # Move both ins and outs to their respective intersections
                # There are actually 2^(in_sets[2] + out_sets[2]) ways to do this!

                a_only = in_sets[2] - in_sets[0]
                b_only = in_sets[2] - in_sets[1]
                a_only_subset = Set(random_subset(a_only)) # a will delete this
                b_only_subset = Set(random_subset(b_only)) # b will delete this

                a_in_add = b_only - b_only_subset # a adds what b does not delete
                a_in_del = a_only_subset
                b_in_add = a_only - a_only_subset # b adds what a does not delete
                b_in_del = b_only_subset

                a_only = out_sets[2] - out_sets[0]
                b_only = out_sets[2] - out_sets[1]
                a_only_subset = Set(random_subset(a_only)) # a will delete this
                b_only_subset = Set(random_subset(b_only)) # b will delete this

                a_out_add = b_only - b_only_subset # a adds what b does not delete
                a_out_del = a_only_subset
                b_out_add = a_only - a_only_subset # b adds what a does not delete
                b_out_del = b_only_subset
                return_values.append([a_in_add, a_in_del, b_in_add, b_in_del, a_out_add, a_out_del, b_out_add, b_out_del])

        return return_values

    # Adds rule id information AND filters out duplicates
    # Id value will be 6 bits:
    # Bit 5: Does node x have in-edges?
    # Bit 4: Does node x have out-edges?
    # Bit 3: Does node x point to node y?
    # Bit 2: Does node y have in-edges?
    # Bit 1: Does node y have out-edges?
    # Bit 0: Does node y point to node x?
    def add_rule_ids_and_filter(self, a, b, best_options):
        just_a = Set([a])
        just_b = Set([b])

        in_sets = [self.in_sets[a] - just_b, self.in_sets[b] - just_a]
        out_sets = [self.out_sets[a] - just_b, self.out_sets[b] - just_a]
        
        a_to_b = a in self.in_sets[b]
        b_to_a = b in self.in_sets[a]

        best_options_with_ids = {}
        for option in best_options:
            # [a_in_add = 0, a_in_del = 1, b_in_add = 2, b_in_del = 3, a_out_add = 4, a_out_del = 5, b_out_add = 6, b_out_del = 7]
            in_a = len((in_sets[0] - option[1]) + option[0]) > 0
            in_b = len((in_sets[1] - option[3]) + option[2]) > 0
            out_a = len((out_sets[0] - option[5]) + option[4]) > 0
            out_b = len((out_sets[1] - option[7]) + option[6]) > 0
            a_score = in_a * 4 + out_a * 2 + a_to_b
            b_score = in_b * 4 + out_b * 2 + b_to_a
            if a_score > b_score:
                best_options_with_ids[(a_score << 3) + b_score] = option
            else:
                best_options_with_ids[(b_score << 3) + a_score] = option]
        return best_options_with_ids
