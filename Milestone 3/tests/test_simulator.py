# tests/test_simulator.py

import networkx as nx
from src.simulator import simulate_broadcast_rounds

def test_star_broadcast():
    # root=0 with children 1,2,3
    T = nx.DiGraph()
    T.add_edges_from([(0,1), (0,2), (0,3)])
    rounds = simulate_broadcast_rounds(T, root=0, terminals={1,2,3})
    # In a star, root can only inform one child per round => 3 rounds
    assert rounds == 3

def test_depth_two_tree():
    # 0→1→3, and 0→2→4
    T = nx.DiGraph()
    edges = [(0,1),(1,3),(0,2),(2,4)]
    T.add_edges_from(edges)
    # terminals {3,4}: both at depth 2
    rounds = simulate_broadcast_rounds(T, root=0, terminals={3,4})
    # Round1: 0→1, Round2: 1→3; but also 0→2 then 2→4 => total 4 rounds under naive one-child-per-round
    # But optimal schedule would be:
    # R1: 0→1
    # R2: 0→2 and 1→3
    # R3: 2→4
    # So 3 rounds
    assert rounds == 3
