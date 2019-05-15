from bitstring import Bits
from bitstring import BitArray
from rule_lib import *

# An edge type interpreter lets you modify a graph while abstractly speaking of edge types.
# From:
# "This edge connects a,b of type 1"
# To:
# "This edge is a directed edge from b to a"
# or to:
# "This edge is a bidirectional edge between b and a"
# or to:
# "This edge is .... whatever you code it to be interpreted as."
class EdgeTypeInterpreter:
    def __init__(self):
        pass

    def add_edge(G, edge_type, node_a, node_b):
        pass

    def remove_edge(G, edge_type, node_a, node_b):
        pass

    # edges_by_type should be the following:
    #   [{node_0: set-of-node_a's-neighbors-with-edges-of-type-0, node_1: set...}, {node_0: set-of...-type-1, ...}, ...]
    # 
    # t should be a Set() of nodes that the rule consists of
    #
    # nodes_with_external_edges_by_type should be the following:
    #   [set-of-nodes-with-external-edges-of-type-0, set-of-...-type-1, ...]
    def make_rule_graph(edges_by_type, t, nodes_with_external_edges_by_type):
        G = nx.DiGraph()

        # Create a node with a self-loop for every edge type.
        # Then chain them together with directed edges.
        name = "type_0"
        G.add_node(name)
        G.add_edge(name, name)
        for i in range(1, len(edges_by_type)):
            prev_name = name
            name = "type_%s" % i
            G.add_node(name)
            G.add_edge(name, name)
            G.add_edge(prev_name, name)

        # Now actually add the nodes in the tuple and the internal edges.
        for node in t:
            G.add_node(t)
            for type_id in range(0, len(edges_by_type)):
                for (node_a, node_b) in edges_by_type[type_id]:
                    if (node_a in t) and (node_b in t):
                        self.add_edge(G, type_id, node_a, node_b)

        for type_id in range(0, len(edges_by_type)):
            type_node_id = "type_%s" % type_id
            for node in nodes_with_external_edges_by_type[type_id]:
                G.add_edge(type_node_id, node)

        return G

# 0 = forward edges (out)
# 1 = backward edges (in)
class BiDirectionalEdgeTypeInterpreter(EdgeTypeInterpreter):
    def __init__(self):
        pass

    def add_edge(G, edge_type, node_a, node_b):
        if edge_type == 0:
            G.add_edge(node_a, node_b)
        elif edge_type == 1:
            G.add_edge(node_b, node_a)
        else:
            print("MAJOR ERROR! INVALID EDGE TYPE %s" % edge_type)

    def remove_edge(G, edge_type, node_a, node_b):
        if edge_type == 0:
            G.remove_edge(node_a, node_b)
        elif edge_type == 1:
            G.remove_edge(node_b, node_a)
        else:
            print("MAJOR ERROR! INVALID EDGE TYPE %s" % edge_type)

# 0 = forward edge only (out)
# 1 = backward edge only (in)
# 2 = both directions
class InOutBothEdgeTypeInterpreter(EdgeTypeInterpreter):
    def __init__(self):
        pass

    def add_edge(G, edge_type, node_a, node_b):
        if edge_type == 0:
            G.add_edge(node_a, node_b)
        elif edge_type == 1:
            G.add_edge(node_b, node_a)
        elif edge_type == 2:
            G.add_edge(node_a, node_b)
            G.add_edge(node_b, node_a)
        else:
            print("MAJOR ERROR! INVALID EDGE TYPE %s" % edge_type)

    def remove_edge(G, edge_type, node_a, node_b):
        if edge_type == 0:
            G.remove_edge(node_a, node_b)
        elif edge_type == 1:
            G.remove_edge(node_b, node_a)
        elif edge_type == 2:
            G.remove_edge(node_a, node_b)
            G.remove_edge(node_b, node_a)
        else:
            print("MAJOR ERROR! INVALID EDGE TYPE %s" % edge_type)

class ApproximateRuleUtils:
    def __init__(self, edge_type_interpreter):
        self.edge_type_interpreter = edge_type_interpreter
        self.rule_lib = RuleLib()

    # Right now this is O(max_degree * |t| * 2^|t|)
    def cheapest_rules_for_tuple(edge_types, t):
        if len(t) > 32:
            print("EXTREME ERROR. ASKING FOR A RULE OF MORE THAN 32 NODES. CANNOT DO BIT MATH.")
            exit(1)

        num_edge_types = len(edge_types)

        t_set = Set(t)
        best_options_found = [[] for i in range(0, num_edge_types)]
        for edge_type_idx in range(0, num_edge_types):
            edge_type = edge_types[edge_type_idx]
            external_neighbors = {} # Maps a node to its external neighbors
            internal_neighbors = {} # Maps an external neighbor to its neighbors in t
            max_possible_cost = 0
            for node in t:
                for neighbor in edge_type[node]:
                    if neighbor in t_set:
                        continue
                    if node not in external_neighbors:
                        external_neighbors[node] = Set([neighbor])
                    else:
                        external_neighbors[node].add(neighbor)
                    if neighbor not in internal_neighbors:
                        internal_neighbors[neighbor] = Set([node])
                    else:
                        internal_neighbors[neighbor].add(node)
                    max_possible_cost += 1

            best_options_found[edge_type_idx] = []
            best_cost_found = max_possible_cost
            for i in range(0, 2**len(t)):
                keep_nodes = Set([t[j] for j in range(0, len(t)) if (i >> j) & 1])
                reject_nodes = Set([t[j] for j in range(0, len(t)) if not ((i >> j) & 1)])

                # Get the cost for the current option.
                current_cost = 0
                for node in reject_nodes:
                    current_cost += len(external_neighbors[node])
                    if current_cost > best_cost_found:
                        break
                if current_cost > best_cost_found:
                    continue
                # O(|t|*dmax*|t|)
                for neighbor, internals in internal_neighbors.items():
                    matches = internals & keep_nodes
                    current_cost += min(len(matches), len(keep_nodes) - len(matches))
                    if current_cost > best_cost_found:
                        break
                if current_cost > best_cost_found:
                    continue
                if current_cost < best_cost_found:
                    best_options_found[edge_type_idx] = []
                    best_cost_found = current_cost

                # If the loop is still here, this is a valid option. Add it to the list.
                deletions = []
                additions = []
                for node in reject_nodes:
                    deletions += [(node, neighbor) for nighbor in external_neighbors[node]]
                for neighbor, internals in internal_neighbors.items():
                    matches = internals & keep_nodes
                    non_matches = keep_nodes - matches
                    if len(matches) <= len(non_matches):
                        deletions += [(node, neighbor) for node in matches]
                    else:
                        additions += [(node, neighbor) for node in non_matches]

                best_options_found[edge_type_idx].append((keep_nodes, deletions, additions))

        rule_ids = Set()
        combined_edge_type_options = []
        sizes = [len(best_options_found[edge_type]) for edge_type in range(0, num_edge_types)]
        counters = [0 for edge_type in range(0, num_edge_types + 1)] # Added a dummy value at the end to make subsequent code simpler.
        counter_idx = 0
        while counter_idx < num_edge_types:
            # Get rule id:
            keep_nodes_by_edge_type = [best_options_found[counters[i]][0] for i in range(0, num_edge_types)]
            rule_id = self.rule_lib.add_rule(self.edge_type_interpreter.make_rule_graph(edge_types, t, keep_nodes_by_edge_type))
            # If the rule id is new for this tuple, add it to our set of results.
            if rule_id not in rule_ids:
                rule_ids.add(rule_id)
                deletions_by_edge_type = [best_options_found[counters[i]][1] for i in range(0, num_edge_types)]
                additions_by_edge_type = [best_options_found[counters[i]][2] for i in range(0, num_edge_types)]
                combined_edge_type_options.append((keep_nodes_by_edge_type, deletions_by_edge_type, additions_by_edge_type))
            
            # Manage the counters
            counter_idx = 0
            counters[counter_idx] += 1
            while counters[counter_idx] == sizes[counter_idx]:
                counters[counter_idx] = 0
                edge_type += 1
                counters[counter_idx] += 1

        return combined_edge_type_options
