import networkx as nx
from test_utils import *

G = nx.read_adjlist("graphs/dblp_cite.edge_list", create_using=nx.DiGraph, nodetype=int)
G = nx.DiGraph(G)
remove_self_loops(G)

single_citation_articles = set(filter(lambda n: G.in_degree(n) == 1, G.nodes()))
no_citation_articles = set(filter(lambda n: G.in_degree(n) == 0, G.nodes()))

single_citations_that_are_cited_by_no_citations = set(filter(lambda n: len(set([i for i, j in G.in_edges(n)]) & no_citation_articles) == 1, single_citation_articles))
any_citations_that_are_cited_by_no_citations = set(filter(lambda n: len(set([i for i, j in G.in_edges(n)]) & no_citation_articles) >= 1, G.nodes()))

print("Single citation articles (cited once) that are cited by no-citation articles: %s" % len(single_citations_that_are_cited_by_no_citations))
print("Single citation articles: %s" % len(single_citation_articles))

print("\n")

print("Num articles cited by at least one no-citation article: %s" % len(any_citations_that_are_cited_by_no_citations))
print("Num articles with at least on citation: %s" % (len(list(G.nodes())) - len(no_citation_articles)))

# Hmmm....

print("\n")

all_that_cite_singles = set(filter(lambda n: len(set([j for i, j in G.out_edges(n)]) & single_citation_articles) >= 1, G.nodes()))
no_citations_that_cite_singles = no_citation_articles & all_that_cite_singles

print("Number of no-citation articles that cite single-citation articles: %s" % len(no_citations_that_cite_singles))
print("Number of articles that cite single-citation articles: %s" % len(all_that_cite_singles))

# More Hmmmm...

print("\n")

count_of_nones_citations = sum([G.out_degree(n) for n in no_citation_articles])
count_of_all_citations = len(G.edges())

count_of_nones_citations_that_are_singles = len(single_citations_that_are_cited_by_no_citations)
count_of_all_citations_that_are_singles = len(single_citation_articles)

print("Percent of non-cited articles' citations that are articles with single citations: %s" % (count_of_nones_citations_that_are_singles / float(count_of_nones_citations)))
print("Percent of any articles' citations that are articles with single citation: %s" % (count_of_all_citations_that_are_singles / float(count_of_all_citations)))

# Now to compare to barabasi albert

print("\n")

print("For a Barabasi Albert Graph...")

G2 = nx.barabasi_albert_graph(len(G.nodes()), 4)
G3 = nx.DiGraph()
for node in G2.nodes():
    G3.add_node(node)
for edge in G2.edges():
    G3.add_edge(max(edge[0], edge[1]), min(edge[0], edge[1]))

single_citation_articles = set(filter(lambda n: G3.in_degree(n) == 1, G3.nodes()))
no_citation_articles = set(filter(lambda n: G3.in_degree(n) == 0, G3.nodes()))

single_citations_that_are_cited_by_no_citations = set(filter(lambda n: len(set([i for i, j in G3.in_edges(n)]) & no_citation_articles) == 1, single_citation_articles))
any_citations_that_are_cited_by_no_citations = set(filter(lambda n: len(set([i for i, j in G3.in_edges(n)]) & no_citation_articles) >= 1, G3.nodes()))

print("Single citation articles that are cited by no-citation articles: %s" % len(single_citations_that_are_cited_by_no_citations))
print("Single citation articles: %s" % len(single_citation_articles))

print("\n")

print("Num articles cited by at least one no-citation article: %s" % len(any_citations_that_are_cited_by_no_citations))
print("Num articles with at least on citation: %s" % (len(list(G.nodes())) - len(no_citation_articles)))

# Hmmm....

print("\n")

all_that_cite_singles = set(filter(lambda n: len(set([j for i, j in G3.out_edges(n)]) & single_citation_articles) >= 1, G3.nodes()))
no_citations_that_cite_singles = no_citation_articles & all_that_cite_singles

print("Number of no-citation articles that cite single-citation articles: %s" % len(no_citations_that_cite_singles))
print("Number of articles that cite single-citation articles: %s" % len(all_that_cite_singles))

# More Hmmmm...

print("\n")

count_of_nones_citations = sum([G3.out_degree(n) for n in no_citation_articles])
count_of_all_citations = len(G3.edges())

count_of_nones_citations_that_are_singles = len(single_citations_that_are_cited_by_no_citations)
count_of_all_citations_that_are_singles = len(single_citation_articles)

print("Percent of non-cited articles' citations that are articles with single citations: %s" % (count_of_nones_citations_that_are_singles / float(count_of_nones_citations)))
print("Percent of any articles' citations that are articles with single citation: %s" % (count_of_all_citations_that_are_singles / float(count_of_all_citations)))
