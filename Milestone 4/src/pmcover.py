from typing import Dict, List, Set, Tuple

def pmcover_half(
    sets: Dict[Tuple[int, int], Set[int]],
    budgets: Dict[int, int],
    k: int
) -> List[Tuple[int, int]]:
    """
    Greedy 1/2‐approximation for the partition‐matroid coverage instance.

    :param sets: mapping from keys (a, c) to the set of terminals covered by c
    :param budgets: mapping from each a to its maximum allowed selections (B*)
    :param k: number of terminals we still need to cover (k_rem)
    :return: list of selected keys (a, c)
    """
    covered: Set[int] = set()
    selected: List[Tuple[int, int]] = []
    used: Dict[int, int] = {a: 0 for a in budgets}

    while len(covered) < k:
        best_key = None
        best_gain = 0

        # Find the key with maximum marginal gain that respects budgets
        for key, items in sets.items():
            a, _ = key
            if used.get(a, 0) >= budgets.get(a, 0):
                continue
            # marginal gain = uncovered items this key would cover
            gain = len(items - covered)
            if gain > best_gain:
                best_gain = gain
                best_key = key

        # stop if no positive gain
        if best_key is None or best_gain == 0:
            break

        # select it
        selected.append(best_key)
        a, _ = best_key
        used[a] = used.get(a, 0) + 1
        covered |= sets[best_key]

    return selected
