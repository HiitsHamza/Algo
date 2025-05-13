# src/graph_loader.py

import networkx as nx

def generate_directed_ER(n: int, p: float, seed: int = None) -> nx.DiGraph:
    """
    Generate a directed Erdős–Rényi graph G(n, p).

    Args:
        n: number of nodes
        p: probability of an edge (for each ordered pair (u,v))
        seed: optional RNG seed

    Returns:
        A NetworkX DiGraph on n nodes.
    """
    return nx.fast_gnp_random_graph(n, p, directed=True, seed=seed)

def generate_directed_clique(n: int) -> nx.DiGraph:
    """
    Generate a complete directed graph on n nodes (all u->v for u!=v).

    Args:
        n: number of nodes

    Returns:
        A NetworkX DiGraph.
    """
    G = nx.DiGraph()
    G.add_nodes_from(range(n))
    for u in range(n):
        for v in range(n):
            if u != v:
                G.add_edge(u, v)
    return G
