import networkx as nx
from networkx import utils
from networkx.algorithms.bipartite.generators import configuration_model
from networkx.algorithms import isomorphism
from networkx.algorithms.shortest_paths.unweighted import all_pairs_shortest_path_length
from networkx.algorithms.components import is_connected
import numpy as np

# Generate first G
using_sequence = False
#sequence = [2, 2, 2, 2, 6, 4, 4, 4, 4]  # Set sequence
#G=nx.configuration_model(sequence)

#G=nx.erdos_renyi_graph(10,0.4)
#G=nx.watts_strogatz_graph(10,3,0.3)
#G=nx.barabasi_albert_graph(10,2)

G=nx.scale_free_graph(100)

# Takes in a digraph and, handling isomorphisms, outputs a number with the following bits:
# zabcdefghijkl
# z: a bit set to 1 to indicate that this is a three-node id
# a: Does node_0 have the external in-edges?
# b: Does node_0 have the external out-edges?
# c: Does node_1 have the external in-edges?
# d: ...
# e:
# f:
# g: Does node_0 point to node_1?
# h: Does node_0 point to node_2?
# i: Does node_1 point to node_0?
# j: Does node_1 point to node_2?
# k: Does node_2 point to node_0?
# l: Does node_2 point to node_1?
def three_nodes_to_id(G, a, b, c):
    three_nodes = [{"id": a, "e_in": 0, "e_out": 0, "i_doub": 0, "i_in": 0, "i_out": 0},
                   {"id": b, "e_in": 0, "e_out": 0, "i_doub": 0, "i_in": 0, "i_out": 0},
                   {"id": c, "e_in": 0, "e_out": 0, "i_doub": 0, "i_in": 0, "i_out": 0}]
    # First we need to get an ordering of the nodes that is impervious to isomorphisms:
    for i in range(0, 3): # O(3 if getting list of neighbors is free)
        for in_edge in G.in_edges(three_nodes[i]["id"]): # O(3 if getting list of neighbors is free)
            if in_edge[0] != three_nodes[(i + 1) % 3]["id"] and in_edge[0] != three_nodes[(i + 2) % 3]["id"]:
                three_nodes[i]["e_in"] = 1
                break
        for out_edge in G.out_edges(three_nodes[i]["id"]): # O(3 if getting list of neighbors is free)
            # print(str(three_nodes[i][0]) + " vs " + str(out_edge[1]))
            if out_edge[1] != three_nodes[(i + 1) % 3]["id"] and out_edge[1] != three_nodes[(i + 2) % 3]["id"]:
                three_nodes[i]["e_out"] = 1
                break
        for j in range(1, 3):
            in_j = G.has_edge(three_nodes[i]["id"], three_nodes[(i + j) % 3]["id"])
            out_j = G.has_edge(three_nodes[(i + j) % 3]["id"], three_nodes[i]["id"])
            if in_j:
                three_nodes[i]["i_in"] += 1
            if out_j:
                three_nodes[i]["i_out"] += 1
            if in_j and out_j:
                three_nodes[i]["i_doub"] += 1

    three_nodes.sort(key=lambda x: (x["e_in"] << 7) + (x["e_out"] << 6) + (x["i_doub"] << 4) + (x["i_in"] << 2) + x["i_out"])

    final_number = (1 << 12) + \
                    (three_nodes[0]["e_in"] << 11) + (three_nodes[0]["e_out"] << 10) + \
                    (three_nodes[1]["e_in"] << 9) + (three_nodes[1]["e_out"] << 8) + \
                    (three_nodes[2]["e_in"] << 7) + (three_nodes[2]["e_out"] << 6)
    first = three_nodes[0]["id"]
    second = three_nodes[1]["id"]
    third = three_nodes[2]["id"]
    final_number += (int(G.has_edge(first, second)) << 5) + (int(G.has_edge(first, third)) << 4)
    final_number += (int(G.has_edge(second, first)) << 3) + (int(G.has_edge(second, third)) << 4)
    final_number += (int(G.has_edge(third, first)) << 1) + int(G.has_edge(third, second))
    return final_number

# Takes in a digraph and, handling isomorphisms, outputs a number with the following bits:
# abcdef
# a: Does node_0 have the external in-edges?
# b: Does node_0 have the external out-edges?
# c: Does node_1 have the external in-edges?
# d: Does node_1 have the external out-edges?
# e: Does node_0 point to node_1?
# f: Does node_1 point to node_0?
def two_nodes_to_id(G, a, b):
    two_nodes = [[a, 0, 0], [b, 0, 0]]
    # First, get their relationship to the outside world.
    # 2 indicates has external in-edges
    # 1 indicates has external out-edges
    for i in range(0, 2): # O(2 if getting list of neighbors is free)
        for in_edge in G.in_edges(two_nodes[i][0]): # O(2 if getting list of neighbors is free)
            if in_edge[0] != two_nodes[(i + 1) % 2][0]:
                two_nodes[i][1] += 2
                break
        for out_edge in G.out_edges(two_nodes[i][0]): # O(2 if getting list of neighbors is free)
            # print(str(three_nodes[i][0]) + " vs " + str(out_edge[1]))
            if out_edge[1] != two_nodes[(i + 1) % 2][0]:
                two_nodes[i][1] += 1
                break
    for i in range(0, 2):
        if G.has_edge(two_nodes[i][0], two_nodes[(i + 1) % 2][0]):
            two_nodes[i][2] += 1

    two_nodes.sort(key=lambda x: (x[1] << 1) + x[2])

    final_number = (two_nodes[0][1] << 4) + (two_nodes[1][1] << 2)
    first = two_nodes[0][0]
    second = two_nodes[1][0]
    final_number += (int(G.has_edge(first, second)) << 1) + (int(G.has_edge(second, first)) << 4)
    return final_number

# Assumes at most 1024 nodes in G
def verify_two_nodes_to_id_works(G):
    checks = {}
    for i in range(0, len(G.nodes())):
        for j in range(0, len(G.nodes())):
            if i == j:
                continue
            nodes = [i, j]
            nodes.sort()
            id_from_ids = (nodes[0] << 10) + nodes[1]
            id_from_function = two_nodes_to_id(G, i, j)
            if id_from_ids in checks:
                if id_from_function != checks[id_from_ids][0]:
                    print("Error!")
                    print(id_from_function)
                    print(checks[id_from_ids])
                    print("i: " + str(checks[id_from_ids][1]) + " j: " + str(checks[id_from_ids][2]))
                    print("i': " + str(i) + " j': " + str(j))
            else:
                checks[id_from_ids] = (id_from_function, i, j)

# Assumes at most 1024 nodes in G
def verify_three_nodes_to_id_works(G):
    checks = {}
    for i in range(0, len(G.nodes())):
        for j in range(0, len(G.nodes())):
            for k in range(0, len(G.nodes())):
                if i == j or i == k or j == k:
                    continue
                nodes = [i, j, k]
                nodes.sort()
                id_from_ids = (nodes[0] << 20) + (nodes[1] << 10) + nodes[2]
                id_from_function = three_nodes_to_id(G, i, j, k)
                if id_from_ids in checks:
                    if id_from_function != checks[id_from_ids][0]:
                        print("Error!")
                        print(id_from_function)
                        print(checks[id_from_ids])
                        print("i: " + str(checks[id_from_ids][1]) + " j: " + str(checks[id_from_ids][2]) + " k: " + str(checks[id_from_ids][3]))
                        print("i': " + str(i) + " j': " + str(j) + " k': " + str(k))
                else:
                    checks[id_from_ids] = (id_from_function, i, j, k)

verify_two_nodes_to_id_works(G)
verify_three_nodes_to_id_works(G)

# Takes a graph and replaces a node with a three-rule:
def replace_node_with_three(G, node_id, three_id, next_id):
    in_edges = G.in_edges(node_id)
    out_edges = G.out_edges(node_id)
    if not three_id & (1 << 11): # If first node has no incoming edges:
        for edge in in_edges:
            G.remove_edge(edge[0], edge[1])
    if not three_id & (1 << 10): # If first node has no outgoing edges:
        for edge in out_edges:
            G.remove_edge(edge[0], edge[1])
    G.add_node(next_id)
    if three_id & (1 << 9): # If second node has incoming edges:
        for edge in in_edges:
            G.add_edge(edge[0], next_id)
    if three_id & (1 << 8): # If second node has outgoing edges:
        for edge in out_edges:
            G.add_edge(next_id, edge[1])
    next_id += 1
    if three_id & (1 << 7): # If third node has incoming edges:
        for edge in in_edges:
            G.add_edge(edge[0], next_id)
    if three_id & (1 << 6): # If third node has outgoing edges:
        for edge in out_edges:
            G.add_edge(next_id, edge[1])

    # TODO: Add code for connecting the three nodes.


# GM = isomorphism.GraphMatcher(G, G_prime)
# actual_iso = GM.is_isomorphic()