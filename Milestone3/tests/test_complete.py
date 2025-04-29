# tests/test_complete.py

import networkx as nx
from src.complete import complete

def test_complete_many_line():
    # Graph: 0->1->2->3
    G = nx.DiGraph()
    edges = [(0,1), (1,2), (2,3)]
    G.add_edges_from(edges)

    root = 0
    # pretend we found two packs [2], [3] but k=1 so pack_size=1
    packings = [[2], [3]]
    cover_edges = []   # not used in MANY case
    k = 1

    T = complete(G, root, packings, cover_edges, k)

    # The tree should be the shortest path 0->1->2
    assert set(T.nodes()) == {0,1,2}
    assert list(T.edges()) == [(0,1),(1,2)]
