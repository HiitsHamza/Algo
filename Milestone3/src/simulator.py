# src/simulator.py

import networkx as nx
from typing import Set, List, Tuple

def simulate_broadcast_rounds(
    tree: nx.DiGraph,
    root: any,
    terminals: Set[any]
) -> int:
    """
    Simulate telephone-model broadcast over a static directed tree.
    Each informed node can call exactly one child per round.
    Returns the number of rounds until all 'terminals' are informed.
    """
    informed = {root}
    to_inform = set(terminals)
    rounds = 0

    # Precompute children in the tree
    children = {u: list(tree.successors(u)) for u in tree.nodes()}

    while to_inform:
        rounds += 1
        new_informed = set()
        # Each informed node can inform one uninformed child (if any)
        for u in list(informed):
            for v in children.get(u, []):
                if v not in informed and v in nx.descendants(tree, u) | {u}:
                    # inform the first available child
                    new_informed.add(v)
                    break
        if not new_informed:
            # no progress ‒ schedule was insufficient
            break
        informed |= new_informed
        to_inform -= new_informed

    return rounds
