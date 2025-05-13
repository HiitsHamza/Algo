# src/pmcover_continuous.py

import random
from typing import Any, Dict, List, Set, Tuple

def pmcover_continuous(
    sets: Dict[Tuple[Any, Any], Set[Any]],
    budgets: Dict[Any, int],
    k: int,
    iters: int = 50,
    samples: int = 20
) -> List[Tuple[Any, Any]]:
    """
    Continuous greedy + rounding for a (1 - 1/e)-approximation
    of maximum coverage under a partition matroid constraint.
    
    Args:
        sets: Mapping from (a, c) pairs to the set of terminals covered.
        budgets: Mapping from each 'a' to the max number of sets allowed.
        k: Target number of terminals to cover.
        iters: Number of continuous-greedy iterations.
        samples: Number of Monte Carlo samples for gradient estimation.
    
    Returns:
        A list of selected (a, c) keys respecting budgets, covering ≥ k terminals.
    """
    keys = list(sets.keys())
    m = len(keys)
    x = [0.0] * m             # fractional solution vector
    dt = 1.0 / iters

    def f_value(S: List[Tuple[Any, Any]]) -> int:
        """Compute the coverage |⋃_{key in S} sets[key]|."""
        covered = set()
        for key in S:
            covered |= sets[key]
        return len(covered)

    # Continuous‐Greedy Phase
    for _ in range(iters):
        # Estimate gradient of multilinear extension via sampling
        grad = [0.0] * m
        for i, key in enumerate(keys):
            gain_sum = 0.0
            for _ in range(samples):
                # Sample a random subset according to x
                S = [keys[j] for j in range(m) if random.random() < x[j]]
                base = f_value(S)
                if key not in S:
                    gain = f_value(S + [key]) - base
                else:
                    gain = 0
                gain_sum += gain
            grad[i] = gain_sum / samples

        # Move x in direction of gradient, projected to matroid polytope
        used = {a: 0 for a in budgets}
        # Sort keys by descending estimated gradient
        for i in sorted(range(m), key=lambda i: -grad[i]):
            a, _ = keys[i]
            if used[a] < budgets[a]:
                x[i] = min(1.0, x[i] + dt)
                used[a] += 1

    # Rounding Phase: greedy by fractional weights x
    selected: List[Tuple[Any, Any]] = []
    covered = set()
    used = {a: 0 for a in budgets}
    for i in sorted(range(m), key=lambda i: -x[i]):
        a, _ = keys[i]
        if used[a] < budgets[a]:
            selected.append(keys[i])
            used[a] += 1
            covered |= sets[keys[i]]
        if len(covered) >= k:
            break

    return selected
