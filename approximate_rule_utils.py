from bitstring import Bits
from bitstring import BitArray

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

class ApproximateRuleUtils:
    def __init__(self, edge_type_interpreter):
        self.edge_type_interpreter = edge_type_interpreter

    # Right now this is O(max_degree * |t| * 2^|t|)
    def cheapest_rules_for_tuple(edge_types, t):
        if len(t) > 32:
            print("EXTREME ERROR. ASKING FOR A RULE OF MORE THAN 32 NODES. CANNOT DO BIT MATH.")
            exit(1)

        t_set = Set(t)
        best_options_found = [[] for i in range(0, len(edge_types))]
        for edge_type_idx in range(0, len(edge_types)):
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

        # TODO: Combine edge type findings into full rules and give them ids.
        combined_edge_type_options = []
