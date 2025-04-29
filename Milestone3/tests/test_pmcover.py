# tests/test_pmcover.py

from src.pmcover import pmcover

def test_pmcover_basic():
    # Define sets mapping (a,c) -> covered items
    sets = {
        ('A', 1): {1, 2},
        ('A', 2): {2, 3},
        ('B', 3): {3, 4},
    }
    # Budgets: can pick at most 1 set with a='A', 1 with a='B'
    budgets = {'A': 1, 'B': 1}
    k = 3

    selected = pmcover(sets, budgets, k)

    # The only way to cover 3 distinct items is to pick one from A and one from B
    assert len(selected) == 2
    assert ('A', 1) in selected or ('A', 2) in selected
    assert ('B', 3) in selected

    # Check that coverage size >= k
    covered = set()
    for key in selected:
        covered |= sets[key]
    assert len(covered) >= k
