# src/complete.py

import math
from typing import Dict, List, Tuple
import networkx as nx

def complete(
    G: nx.DiGraph,
    root: int,
    packs: List[List[int]],
    cover_edges: List[Tuple[int, int]],
    cover_map: Dict[int, List[int]],
    k: int
) -> nx.DiGraph:
    """
    Stitch together the greedy-packing subtrees and the selected cover edges
    into a single directed multicast tree rooted at `root`.

    cover_map maps each cover-edge target `c` to the list of terminals it should cover.
    """
    T = nx.DiGraph()
    T.add_node(root)

    rho = math.ceil(math.sqrt(k))

    # CASE A: enough greedy packs to cover k without any cover_edges
    if len(packs) >= rho:
        reps = [pack[0] for pack in packs[:rho]]
        for rep in reps:
            try:
                path = nx.shortest_path(G, source=root, target=rep)
                T.add_nodes_from(path)
                T.add_edges_from(zip(path, path[1:]))
            except nx.NetworkXNoPath:
                # Skip if no path exists
                continue
        return T

    # CASE B: stitch both packs and cover_edges
    # 1) Connect root → each pack and pack → its terminals
    for pack in packs:
        rep = pack[0]
        # path root → rep
        try:
            path = nx.shortest_path(G, source=root, target=rep)
            T.add_nodes_from(path)
            T.add_edges_from(zip(path, path[1:]))
            # paths rep → each terminal in pack
            for term in pack:
                if term == rep:
                    continue
                try:
                    subpath = nx.shortest_path(G, source=rep, target=term)
                    T.add_nodes_from(subpath)
                    T.add_edges_from(zip(subpath, subpath[1:]))
                except nx.NetworkXNoPath:
                    continue
        except nx.NetworkXNoPath:
            # Skip this pack if no path from root to rep
            continue

    # 2) Add each cover-edge (a→c) and c → its cover_map[c] terminals
    for (a, c) in cover_edges:
        # Skip if a is not in tree or c is not in graph
        if a not in T or c not in G:
            continue
            
        # Add the single edge a → c
        T.add_edge(a, c)
        # For each terminal that c is responsible for, stitch a shortest path
        for term in cover_map.get(c, []):
            # Check if terminal exists in G before finding path
            if term not in G:
                continue
                
            try:
                # path c → term
                subpath = nx.shortest_path(G, source=c, target=term)
                T.add_nodes_from(subpath)
                T.add_edges_from(zip(subpath, subpath[1:]))
            except nx.NetworkXNoPath:
                # If no path exists, skip this terminal
                continue

    return T
