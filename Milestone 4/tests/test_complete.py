import networkx as nx
import pytest
from src.complete import complete

def build_tiny_graph():
    """
    Construct a small directed graph:
    0 → 1 → 2
    0 → 3
    Terminals: {2, 3}
    """
    G = nx.DiGraph()
    edges = [(0,1), (1,2), (0,3)]
    G.add_edges_from(edges)
    return G

def test_complete_with_sufficient_packs():
    """
    If packs alone cover k, complete should create paths from root to pack reps.
    """
    G = build_tiny_graph()
    root = 0
    packs = [[2], [3]]  # rho=ceil(sqrt(2))=2, so two packs suffice
    cover_edges = []    # ignored
    cover_map = {}
    k = 2
    T = complete(G, root, packs, cover_edges, cover_map, k)
    # T should contain paths 0→1→2 and 0→3
    assert nx.has_path(T, 0, 2)
    assert nx.has_path(T, 0, 3)
    # No extra nodes
    assert set(T.nodes()) <= set(G.nodes())

def test_complete_with_packs_and_cover():
    """
    If packs < rho, integrate cover_edges and cover_map.
    """
    G = build_tiny_graph()
    root = 0
    packs = [[2]]     # only one pack, rho=2 so need cover_edges
    # Simulate cover_edges selecting edge (0,3) covering terminal 3
    cover_edges = [(0,3)]
    cover_map = {3: [3]}
    k = 2
    T = complete(G, root, packs, cover_edges, cover_map, k)
    # T must cover both terminals
    assert nx.has_path(T, 0, 2)
    assert nx.has_path(T, 0, 3)
    # T remains acyclic
    assert nx.is_directed_acyclic_graph(T)

def test_complete_respects_root_only():
    """
    Even if cover_map contains extraneous nodes, only connected ones appear.
    """
    G = build_tiny_graph()
    root = 0
    packs = []
    cover_edges = [(0,3)]
    cover_map = {3: [3, 99]}  # node 99 doesn't exist in G
    k = 1
    T = complete(G, root, packs, cover_edges, cover_map, k)
    # Only valid nodes appear
    assert 99 not in T.nodes()
    assert 3 in T.nodes()
    assert nx.has_path(T, 0, 3)

def test_complete_empty():
    """
    With no packs and no cover, complete returns only the root node.
    """
    G = build_tiny_graph()
    root = 0
    packs = []
    cover_edges = []
    cover_map = {}
    k = 1
    T = complete(G, root, packs, cover_edges, cover_map, k)
    assert set(T.nodes()) == {0}
