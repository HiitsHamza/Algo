import pytest
from src.pmcover_continuous import pmcover_continuous

def test_continuous_simple_match_half():
    """
    On the same simple partition, continuous-greedy with minimal iters/samples
    should cover at least as much as pmcover_half (i.e., ≥ k/2).
    """
    sets = {
        ('a', 1): {1},
        ('a', 2): {2},
        ('b', 3): {3},
        ('b', 4): {4},
    }
    budgets = {'a': 1, 'b': 1}
    k = 2
    chosen = pmcover_continuous(sets, budgets, k, iters=5, samples=5)
    covered = set().union(*(sets[key] for key in chosen))
    # continuous should cover at least one element (half of k)
    assert len(covered) >= 1

def test_continuous_respects_budget_and_cap():
    """
    Ensure we never exceed budgets and we stop once k elements are covered.
    """
    sets = {
        ('a', 1): {1},
        ('a', 2): {2},
        ('b', 3): {3},
    }
    budgets = {'a': 1, 'b': 1}
    k = 2
    chosen = pmcover_continuous(sets, budgets, k, iters=3, samples=3)
    # At most 2 picks and respects budget 'a':1, 'b':1
    assert len(chosen) <= 2
    assert sum(1 for key in chosen if key[0] == 'a') <= 1
    assert sum(1 for key in chosen if key[0] == 'b') <= 1

def test_continuous_zero_gain():
    """
    If all sets cover the same items, continuous-greedy should pick only up to budget.
    """
    sets = {
        ('a', 1): {1, 2},
        ('a', 2): {1, 2},
    }
    budgets = {'a': 1}
    k = 2
    chosen = pmcover_continuous(sets, budgets, k, iters=4, samples=4)
    # Should pick only one because budget a=1
    assert len(chosen) == 1
