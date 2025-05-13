# src/greedy_packing.py

import networkx as nx
import math
from collections import deque

def find_greedy_packing(G: nx.DiGraph, root, terminals: set, k: int, D_star: int):
    """
    Extract up to ceil(sqrt(k)) packs of terminals, each pack containing
    exactly ceil(sqrt(k)) terminals reachable within depth D_star in G,
    by finding disjoint BFS-based subtrees.

    Returns:
        packings: List[List[node]]  # each inner list is the chosen terminals
    """
    # Already-informed root removed; C = candidates
    C = set(G.nodes()) - {root}
    # How many terminals per pack, and how many packs to find
    pack_size = math.ceil(math.sqrt(k))
    max_packs = pack_size

    packings = []

    def bfs_up_to_depth(src):
        # BFS from src within C up to depth D_star,
        # returns parent pointers + list of terminals found
        parent = {src: None}
        depth = {src: 0}
        q = deque([src])
        found = []
        while q:
            u = q.popleft()
            if depth[u] >= D_star:
                continue
            for v in G.successors(u):
                if v in C and v not in parent:
                    parent[v] = u
                    depth[v] = depth[u] + 1
                    q.append(v)
                    if v in terminals:
                        found.append(v)
                        if len(found) >= pack_size:
                            return parent, found
        return parent, found

    # Greedily extract up to max_packs packs
    while len(packings) < max_packs:
        found_any = False
        for c in list(C):
            parent, found = bfs_up_to_depth(c)
            if len(found) >= pack_size:
                # Select exactly pack_size terminals
                chosen = found[:pack_size]
                # Remove those terminals AND their path nodes so packs stay disjoint
                to_remove = set()
                for t in chosen:
                    v = t
                    while v is not None and v not in to_remove:
                        to_remove.add(v)
                        v = parent[v]
                C -= to_remove
                packings.append(chosen)
                found_any = True
                break
        if not found_any:
            break

    return packings
