import networkx as nx
from typing import Optional

def generate_directed_ER(n: int, p: float, seed: Optional[int] = None) -> nx.DiGraph:
    """
    Generate a random directed Erdős–Rényi graph G(n, p).
    
    Each possible directed edge (u→v) is included independently with probability p.
    
    :param n: number of nodes (labeled 0..n-1)
    :param p: edge-creation probability
    :param seed: optional random seed for reproducibility
    :return: a networkx.DiGraph instance
    """
    return nx.gnp_random_graph(n, p, seed=seed, directed=True)

def generate_directed_clique(n: int) -> nx.DiGraph:
    """
    Generate a directed clique on n nodes (every ordered pair except self-loops).
    
    :param n: number of nodes (labeled 0..n-1)
    :return: a networkx.DiGraph instance with edges u→v for all u != v
    """
    G = nx.DiGraph()
    G.add_nodes_from(range(n))
    for u in range(n):
        for v in range(n):
            if u != v:
                G.add_edge(u, v)
    return G
