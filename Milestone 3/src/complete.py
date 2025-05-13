# src/complete.py

import networkx as nx
import math
from typing import Any, List, Tuple

def complete(
    G: nx.DiGraph,
    root: Any,
    packings: List[List[Any]],
    cover_edges: List[Tuple[Any, Any]],
    k: int
) -> nx.DiGraph:
    """
    Build the final multicast tree:
      - If we found >= ceil(sqrt(k)) disjoint packs, connect root via
        shortest paths to each pack's representative.
      - Otherwise, simply include the chosen cover_edges (a,c).

    Args:
      G: original directed graph
      root: broadcast root
      packings: list of terminal-lists from greedy_packing
      cover_edges: list of (a,c) from pmcover
      k: target terminals

    Returns:
      A DiGraph containing exactly the edges of the multicast tree.
    """
    tree = nx.DiGraph()
    pack_size = math.ceil(math.sqrt(k))

    if len(packings) >= pack_size:
        # MANY TREES case
        reps = [p[0] for p in packings[:pack_size]]
        edges = set()
        for rep in reps:
            # shortest path from root to rep
            path = nx.shortest_path(G, source=root, target=rep)
            edges.update(zip(path, path[1:]))
        tree.add_edges_from(edges)

    else:
        # FEW TREES fallback: just use the cover_edges
        tree.add_edges_from(cover_edges)

    return tree
