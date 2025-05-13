import pytest
from src.pmcover_lazy import pmcover_lazy

def test_lazy_simple_match_half():
    """
    On a basic partition, lazy-greedy should cover at least as much as half-approx (≥ k/2).
    """
    sets = {
        ('a', 1): {1},
        ('a', 2): {2},
        ('b', 3): {3},
        ('b', 4): {4},
    }
    budgets = {'a': 1, 'b': 1}
    k = 2
    chosen = pmcover_lazy(sets, budgets, k)
    covered = set().union(*(sets[key] for key in chosen))
    assert len(covered) >= 1  # at least half of k

def test_lazy_respects_budget():
    """
    Lazy-greedy must never exceed the per-part budgets.
    """
    sets = {
        ('a', 1): {1},
        ('a', 2): {2},
        ('b', 3): {3},
    }
    budgets = {'a': 1, 'b': 1}
    k = 2
    chosen = pmcover_lazy(sets, budgets, k)
    # Count selections per part
    count_a = sum(1 for key in chosen if key[0] == 'a')
    count_b = sum(1 for key in chosen if key[0] == 'b')
    assert count_a <= budgets['a']
    assert count_b <= budgets['b']

def test_lazy_stops_when_no_gain():
    """
    If no new gain is possible, lazy-greedy should exit early.
    """
    sets = {
        ('a', 1): {1,2},
        ('a', 2): {1,2},
    }
    budgets = {'a': 1}
    k = 2
    chosen = pmcover_lazy(sets, budgets, k)
    covered = set().union(*(sets[key] for key in chosen))
    # Should cover both items in one pick, then stop
    assert covered == {1,2}
    assert len(chosen) == 1

def test_lazy_empty_instance():
    """
    If k=0 or sets empty, result is empty list.
    """
    assert pmcover_lazy({}, {}, 0) == []
    # If no sets but k>0, still returns empty
    assert pmcover_lazy({}, {}, 3) == []
