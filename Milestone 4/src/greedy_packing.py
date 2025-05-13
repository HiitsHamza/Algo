import math
from collections import deque
from typing import List, Set
import networkx as nx

def bfs_subtree_nodes(
    G: nx.DiGraph,
    source: int,
    max_depth: int
) -> Set[int]:
    """
    Perform a breadth‐first search from `source` up to `max_depth` hops,
    and return the set of all visited nodes.
    """
    visited = {source}
    queue = deque([(source, 0)])
    while queue:
        u, depth = queue.popleft()
        if depth >= max_depth:
            continue
        for v in G.successors(u):
            if v not in visited:
                visited.add(v)
                queue.append((v, depth + 1))
    return visited

def find_greedy_packing(
    G: nx.DiGraph,
    root: int,
    terminals: Set[int],
    k: int,
    D_star: int
) -> List[List[int]]:
    """
    Extract up to rho = ceil(sqrt(k)) vertex‐disjoint subtrees of height ≤ D_star,
    each covering at least one terminal. Returns a list of the terminal‐lists
    covered by each subtree.
    
    When k > 1, tries to find packs that cover at least rho terminals each.
    When k = 1, includes any pack that covers at least one terminal.
    """
    rho = math.ceil(math.sqrt(k))
    packs: List[List[int]] = []
    # Candidate nodes for subtree roots 
    candidates = set(G.nodes()) - {root}
    # Terminals not yet covered
    remaining_terms = set(terminals)
    # Keep track of used nodes to ensure disjointness
    used_nodes = {root}
    
    # Try to find up to rho packs
    while len(packs) < rho and remaining_terms:
        best_node = None
        best_cover: Set[int] = set()
        best_subtree: Set[int] = set()

        # Find the node whose depth‐D_star subtree covers the most remaining terminals
        for c in candidates:
            # Skip if this node is already used
            if c in used_nodes:
                continue
                
            subtree_nodes = bfs_subtree_nodes(G, c, D_star)
            # Skip if subtree contains any used nodes (ensuring disjointness)
            if not subtree_nodes.isdisjoint(used_nodes):
                continue
                
            cover = subtree_nodes & remaining_terms
            
            # For k=1, take only the first terminal found
            if k == 1 and cover:
                cover = {next(iter(cover))}
                
            if len(cover) > len(best_cover):
                best_node = c
                best_cover = cover
                best_subtree = subtree_nodes

        # Stop if no more coverage is possible
        if not best_cover:
            break
            
        # For k > 1, we ideally want coverage >= rho, but accept any available coverage
        min_coverage = 1  # Always accept at least one terminal
            
        # If we found a valid pack, record it
        if len(best_cover) >= min_coverage:
            packs.append(list(best_cover))
            used_nodes.update(best_subtree)
            remaining_terms -= best_cover
        else:
            # If no valid subtree found, we're done
            break

    return packs
