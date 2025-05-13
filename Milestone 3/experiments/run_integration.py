# experiments/run_integration.py

import random
import networkx as nx
from src.graph_loader import complete_graph
from src.greedy_packing import find_greedy_packing
from src.complete import complete
from src.simulator import simulate_broadcast_rounds


def run_integration():
    # Parameters
    n = 20
    root = 0
    # Use a complete graph to guarantee greedy packing
    G = complete_graph(n)

    # Define terminals and target k
    terminals = set(range(1, 11))  # nodes 1..10
    k = 4
    D_star = 1  # one round depth suffices in complete graph

    # 1. Greedy packing
    packings = find_greedy_packing(G, root, terminals, k, D_star)
    print("Greedy packing found:", packings)

    # 2. Complete construction (Many Trees case expected)
    T = complete(G, root, packings, cover_edges=[], k=k)
    print("Multicast tree edges:", list(T.edges()))

    # 3. Simulate rounds to inform k
    rounds = simulate_broadcast_rounds(T, root, terminals)
    print(f"Rounds needed to inform {k} terminals:", rounds)

    assert rounds <= k, "Integration test failed: too many rounds"

if __name__ == '__main__':
    run_integration()
