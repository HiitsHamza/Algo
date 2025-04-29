import networkx as nx
from src.greedy_packing import find_greedy_packing

def test_simple_line_graph():
    # Build a directed path  r → 1 → 2 → 3 → 4
    G = nx.DiGraph()
    edges = [(0,1),(1,2),(2,3),(3,4)]
    G.add_edges_from(edges)
    root = 0
    terminals = {2,3,4}
    # k = 1: sqrt(k)=1 target; D_star=2 allows reaching nodes 2 or 3 in 2 steps
    packs = find_greedy_packing(G, root, terminals, k=1, D_star=2)
    # We expect exactly one subtree, of size 1 (one terminal)
    assert len(packs) == 1
    assert len(packs[0]) == 1
    assert next(iter(packs[0])) in {2,3}
