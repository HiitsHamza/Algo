import networkx as nx
import pytest
from src.graph_loader import generate_directed_ER, generate_directed_clique

def test_ER_node_count_and_type():
    """ER graph should have exactly n nodes and be directed."""
    n = 10
    G = generate_directed_ER(n, 0.5, seed=123)
    assert isinstance(G, nx.DiGraph)
    assert G.number_of_nodes() == n

def test_ER_reproducibility_with_seed():
    """Using the same seed should produce identical edge sets."""
    G1 = generate_directed_ER(20, 0.3, seed=42)
    G2 = generate_directed_ER(20, 0.3, seed=42)
    assert sorted(G1.edges()) == sorted(G2.edges())

def test_ER_edge_probability():
    """
    For p=1.0, ER should be a complete digraph (minus self-loops).
    For p=0.0, it should have no edges.
    """
    n = 8
    G_full = generate_directed_ER(n, 1.0, seed=7)
    # full directed clique has n*(n-1) edges
    assert G_full.number_of_edges() == n * (n - 1)

    G_empty = generate_directed_ER(n, 0.0, seed=7)
    assert G_empty.number_of_edges() == 0

def test_clique_node_count_and_edges():
    """Clique graph should have every possible directed edge except self-loops."""
    n = 15
    G = generate_directed_clique(n)
    assert isinstance(G, nx.DiGraph)
    assert G.number_of_nodes() == n
    # expected edges = n*(n-1)
    assert G.number_of_edges() == n * (n - 1)
    # spot-check a few edges and non-edges
    for u in [0, n//2, n-1]:
        for v in [0, 1, n//3]:
            if u != v:
                assert G.has_edge(u, v)
            else:
                assert not G.has_edge(u, v)
