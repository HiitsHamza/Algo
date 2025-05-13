import pytest
from src.pmcover import pmcover_half

def test_half_on_simple_partition():
    """
    Universe U = {1,2,3,4}, partition a->{(a,1),(a,2)}, b->{(b,3),(b,4)},
    budgets: a:1, b:1, k=2. Optimal coverage = 4 by picking both (a,1)&(b,3) etc.
    Half-approx should cover at least 2 elements.
    """
    sets = {
        ('a', 1): {1},
        ('a', 2): {2},
        ('b', 3): {3},
        ('b', 4): {4},
    }
    budgets = {'a': 1, 'b': 1}
    k = 2
    chosen = pmcover_half(sets, budgets, k)
    covered = set().union(*(sets[key] for key in chosen))
    assert len(chosen) <= 2
    assert len(covered) >= 1  # half-approx covers ≥ k/2 = 1
    # Should be able to cover at least one element per budget
    assert all(chosen.count(key) == 1 for key in chosen)

def test_half_stops_when_no_gain():
    """
    If no sets cover any new elements, pmcover_half should exit quickly.
    """
    sets = {
        ('a', 1): {1,2},
        ('a', 2): {1,2},
    }
    budgets = {'a': 1}
    k = 2
    # First pick covers {1,2}, next picks have zero gain.
    chosen = pmcover_half(sets, budgets, k)
    covered = set().union(*(sets[key] for key in chosen))
    assert covered == {1,2}
    assert len(chosen) == 1  # budget exhausted

def test_half_respects_budget():
    """
    If budgets[a]=0, no set from part 'a' can be chosen.
    """
    sets = {
        ('a', 1): {1},
        ('b', 2): {2},
    }
    budgets = {'a': 0, 'b': 1}
    k = 1
    chosen = pmcover_half(sets, budgets, k)
    # Only 'b' may be chosen
    assert all(key[0] != 'a' for key in chosen)
