import networkx as nx
import pytest
from src.greedy_packing import find_greedy_packing

def build_directed_path(n):
    """Helper: build a directed path 0→1→2→…→n-1."""
    G = nx.DiGraph()
    G.add_nodes_from(range(n))
    edges = [(i, i+1) for i in range(n-1)]
    G.add_edges_from(edges)
    return G

def test_simple_path_k1_D2():
    """
    On a path of length 4 (0→1→2→3→4), root=0,
    terminals={2,3,4}, k=1, D*=2 should find exactly one pack
    of size 1 (either covers node 2 or 3), rho = ceil(sqrt(1)) = 1.
    """
    G = build_directed_path(5)
    root = 0
    terminals = {2, 3, 4}
    packs = find_greedy_packing(G, root, terminals, k=1, D_star=2)
    # rho = 1 so exactly 1 pack of size >=1
    assert len(packs) == 1
    assert len(packs[0]) == 1
    assert packs[0][0] in {2, 3}

def test_path_k4_D3():
    """
    On the same path, if k=4, rho=ceil(sqrt(4))=2.
    We can extract up to 2 disjoint subtrees of depth 3:
    one rooted at 1 covers {1,2,3,4} but terminals only {2,3,4};
    second pack should fail (no more coverage).
    """
    G = build_directed_path(6)
    root = 0
    terminals = {2, 3, 4, 5}
    packs = find_greedy_packing(G, root, terminals, k=4, D_star=3)
    # We expect at least one pack covering >=2 terminals
    assert len(packs) >= 1
    # The first pack must cover at least rho=2 terminals
    assert len(packs[0]) >= 2

def test_vertex_disjointness():
    """
    Ensure that packs returned are vertex-disjoint.
    We build a small tree with two branches.
    """
    G = nx.DiGraph()
    #     0
    #    / \
    #   1   2
    #  /     \
    # 3       4
    edges = [(0,1),(1,3),(0,2),(2,4)]
    G.add_edges_from(edges)
    root = 0
    terminals = {3,4}
    packs = find_greedy_packing(G, root, terminals, k=2, D_star=2)
    # rho=ceil(sqrt(2))=2, but only two terminals available;
    # both should be covered in two disjoint packs of size=1 each
    assert len(packs) == 2
    # check disjoint
    all_nodes = set()
    for pack in packs:
        pack_nodes = set(pack)
        assert all_nodes.isdisjoint(pack_nodes)
        all_nodes |= pack_nodes
