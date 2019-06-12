import networkx as nx
import argparse
from full_approximate_rule_miner import *
from test_utils import *

parser = argparse.ArgumentParser()
parser.add_argument("rule_min", type=int, help="Minimum rule size")
parser.add_argument("rule_max", type=int, help="Maximum rule size")
parser.add_argument("graph_type", help="The graph type. Valid values are watts_strogats, n_tree, and n_tree_of_k_rings")
parser.add_argument("size", type=int, help="The number of nodes in the graph.")
parser.add_argument("n", type=int, help="A graph parameter. For watts_strogats, specifies number of neighbors. For the trees, specifies number of children.")
parser.add_argument("-k", type=int, help="A graph parameter. For n_tree_of_k_rings, specifies the ring size.")
parser.add_argument("--bidirected", help="Add if the graph should be bidirected. Currently just for watts_strogatz")
args = parser.parse_args()
if args.graph_type not in ["watts_strogatz", "n_tree", "n_tree_of_k_rings"]:
    print("ERROR: Unknown graph type %s. Aborting." % args.graph_type)
    exit(2)
if args.graph_type == "watts_strogatz" and args.k:
    print("INFO: k was specified but is not used in watts_strogatz")
if args.graph_type == "n_tree" and args.k:
    print("INFO: k was specified but is not used in an n_tree")
if args.graph_type == "n_tree_of_k_rings" and not args.k:
    print("ERROR: need k for n_tree_of_k_rings. Aborting.")
    exit(2)

G = None
if args.graph_type == "n_tree":
    G = n_ary_tree(args.size, args.n) 
elif args.graph_type == "n_tree_of_k_rings":
    G = n_ary_tree_of_k_rings(args.size, args.n, args.k)
elif args.graph_type == "watts_strogatz":
    #rewiring_prob = 0
    #if len(sys.argv) > 7:
    #    rewiring_prob = float(sys.argv[7])
    bidirected = args.bidirected is not None
    G = watts_strogatz(args.size, args.n, 0, bidirected)

rm = FullApproximateRuleMiner(G, args.rule_min, args.rule_max)

while not rm.done():
    best_rule = rm.determine_best_rule()
    rm.contract_valid_tuples(best_rule)
rm.cost_comparison()
