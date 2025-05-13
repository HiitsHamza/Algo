# src/pmcover.py

from typing import Any, Dict, List, Set, Tuple

def pmcover(
    sets: Dict[Tuple[Any, Any], Set[Any]],
    budgets: Dict[Any, int],
    k: int
) -> List[Tuple[Any, Any]]:
    """
    Greedy 1/2-approximation for max coverage under a partition matroid.
    
    Args:
        sets: mapping from a pair-id (a, c) to the set of terminals it covers.
        budgets: mapping from each 'a' to the maximum number of sets we can pick with that a.
        k: target number of terminals to cover.
    
    Returns:
        A list of selected keys (a, c) whose union of coverage has size >= k
        or as close as possible under the budgets.
    """
    covered: Set[Any] = set()
    selected: List[Tuple[Any, Any]] = []
    budgets_remaining = budgets.copy()

    while len(covered) < k:
        best_gain = 0
        best_key = None

        # Find the set with maximum marginal gain that respects budgets
        for key, items in sets.items():
            a, _c = key
            if budgets_remaining.get(a, 0) <= 0 or key in selected:
                continue
            gain = len(items - covered)
            if gain > best_gain:
                best_gain = gain
                best_key = key

        # Stop if no further progress is possible
        if best_key is None or best_gain == 0:
            break

        # Select it
        selected.append(best_key)
        covered |= sets[best_key]
        a, _ = best_key
        budgets_remaining[a] -= 1

    return selected
