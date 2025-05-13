import networkx as nx
import pytest
from src.simulator import simulate_broadcast_rounds

def build_chain_tree(length: int) -> nx.DiGraph:
    """
    Build a simple directed chain 0→1→2→...→length
    """
    T = nx.DiGraph()
    nodes = list(range(length + 1))
    T.add_nodes_from(nodes)
    edges = [(i, i + 1) for i in range(length)]
    T.add_edges_from(edges)
    return T

def test_chain_depth_rounds():
    """
    In a chain of length L, it takes exactly L rounds
    to inform the last node in the telephone model.
    """
    L = 5
    T = build_chain_tree(L)
    root = 0
    terminals = {L}
    rounds = simulate_broadcast_rounds(T, root, terminals)
    assert rounds == L

def build_bush_tree(depth: int, branching: int) -> nx.DiGraph:
    """
    Build a full k-ary tree of given depth.
    Root at 0, each node at level < depth has 'branching' children.
    """
    T = nx.DiGraph()
    node_id = 0
    T.add_node(node_id)
    current_level = [node_id]
    for _ in range(depth):
        next_level = []
        for u in current_level:
            for _ in range(branching):
                node_id += 1
                T.add_edge(u, node_id)
                next_level.append(node_id)
        current_level = next_level
    return T

def test_bush_tree_rounds():
    """
    In a full k-ary tree of depth D, with unlimited branching,
    the telephone model informs one new branch per round per informed node,
    so it finishes in exactly D rounds to inform all leaves.
    """
    D = 3
    B = 4
    T = build_bush_tree(D, B)
    root = 0
    # leaves are all nodes at last level
    leaves = {n for n in T.nodes() if T.out_degree(n) == 0}
    rounds = simulate_broadcast_rounds(T, root, leaves)
    assert rounds == D

def test_no_progress_stops_early():
    """
    If the tree has an isolated terminal not reachable, simulator stops early.
    """
    T = nx.DiGraph()
    T.add_edges_from([(0,1), (1,2)])
    root = 0
    terminals = {2, 99}  # 99 is not in the tree
    rounds = simulate_broadcast_rounds(T, root, terminals)
    # informs 2 in 2 rounds, then cannot inform 99, so stops at 2
    assert rounds == 2

def test_empty_terminal_set():
    """
    If terminals set is empty or already contains root, rounds = 0.
    """
    T = build_chain_tree(3)
    root = 0
    assert simulate_broadcast_rounds(T, root, set()) == 0
    # root already informed
    assert simulate_broadcast_rounds(T, root, {0}) == 0
