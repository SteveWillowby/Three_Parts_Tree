from bitstring import Bits
from bitstring import BitArray

class ApproximateRuleUtils:
    
    def cheapest_rules_for_tuple(in_edges, out_edges, t):
        edge_types = [in_edges, out_edges]
        return self.cheapest_rules_for_tuple_helper(edge_types, t)

    # Right now this is O(max_degree * |t| * 2^|t|)
    def cheapest_rules_for_tuple_helper(edge_types, t):
        if len(t) > 32:
            print("EXTREME ERROR. ASKING FOR A RULE OF MORE THAN 32 NODES. CANNOT DO BIT MATH.")
            exit(1)

        # TODO: Add canonical node GROUP ordering by automorphism group

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
            best_options_ids = Set()
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
                    best_options_ids = Set()
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

                # Now we need to find the bits to represent this rule.
                id_for_type = self.rule_id_for_single_edge_type(edge_type, keep_nodes, reject_nodes)
                if id_for_type not in best_options_ids:
                    best_options_found[edge_type_idx].append((id_for_type, deletions, additions))
                    best_options_ids.add(id_for_type)

        # TODO: Combine edge type findings into full rules.
        combined_edge_type_options = []
        

    def rule_id_for_single_edge_type(edge_type, keep, reject):
        # TODO: Implement this.
        pass 
