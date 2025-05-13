# src/pmcover_lazy.py

import heapq
from typing import Dict, List, Set, Tuple

def pmcover_lazy(
    sets: Dict[Tuple[int, int], Set[int]],
    budgets: Dict[int, int],
    k: int
) -> List[Tuple[int, int]]:
    """
    Lazy‐greedy 1/2‐approximation for the partition‐matroid coverage instance.
    Uses a max‐heap of (neg_gain, key) and only recomputes gain when it becomes stale.
    """
    covered: Set[int] = set()
    selected: List[Tuple[int, int]] = []
    used: Dict[int, int] = {a: 0 for a in budgets}

    # Initialize heap with estimated gains = full set sizes
    heap: List[Tuple[int, Tuple[int,int]]] = [
        (-len(items), key) for key, items in sets.items()
    ]
    heapq.heapify(heap)

    while len(covered) < k and heap:
        neg_est, key = heapq.heappop(heap)
        a, _ = key
        # Compute true marginal gain
        true_gain = len(sets[key] - covered)
        # If this matches the previous estimate and budget allows, select
        if -neg_est == true_gain and used[a] < budgets[a]:
            selected.append(key)
            used[a] += 1
            covered |= sets[key]
        # Otherwise push back with updated gain
        elif used[a] < budgets[a] and true_gain > 0:
            heapq.heappush(heap, (-true_gain, key))
        # else discard (no budget or no gain)

    return selected
