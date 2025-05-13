#!/usr/bin/env python3
"""
Quick end-to-end “smoke” integration on a small directed clique.
Verifies that each stage runs without errors and prints plausible metrics.
"""

import os
import sys
import time
import math
import random

# ensure project root (parent of experiments/) is on PYTHONPATH
ROOT = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
sys.path.insert(0, ROOT)

import networkx as nx

from src.graph_loader import generate_directed_clique
from src.greedy_packing import find_greedy_packing
from src.pmcover import pmcover_half
from src.pmcover_continuous import pmcover_continuous
from src.pmcover_lazy import pmcover_lazy
from src.complete import complete
from src.simulator import simulate_broadcast_rounds
from collections import deque

def build_cover_instance(G, root, terminals, packs, D_star, k):
    # same helper as demo
    covered_by_packs = set().union(*packs) if packs else set()
    A = {root} | covered_by_packs
    C = set(G.nodes()) - A
    rho = math.ceil(math.sqrt(k))
    budgets = {a: rho for a in A}
    sets = {}
    cover_map = {}
    for a in A:
        for c in G.successors(a):
            if c not in C:
                continue
            visited = {c}
            queue = deque([(c, 0)])
            while queue:
                u, d = queue.popleft()
                if d >= D_star:
                    continue
                for v in G.successors(u):
                    if v in C and v not in visited:
                        visited.add(v)
                        queue.append((v, d + 1))
            cover = visited & terminals
            if cover:
                sets[(a, c)] = cover
                cover_map[c] = list(cover)
    return sets, budgets, cover_map

def main():
    # parameters for a small smoke test
    n = 10
    D_star = 3
    t_ratio = 0.5
    k_ratio = 0.4
    iters = 10
    samples = 5

    print(f"\n=== RUNNING INTEGRATION TEST (clique n={n}) ===\n")

    # 1) build clique
    G = generate_directed_clique(n)
    root = 0
    nodes = list(G.nodes())

    # 2) pick terminals
    t = max(1, int(t_ratio * n))
    terminals = set(random.sample(nodes, t))
    if root in terminals:
        terminals.remove(root)
    t = len(terminals)

    # 3) compute k
    k = max(1, int(k_ratio * t))

    print(f"Terminals={t}, k={k}, D*={D_star}")

    # 4) greedy packing
    t0 = time.perf_counter()
    packs = find_greedy_packing(G, root, terminals, k, D_star)
    t1 = time.perf_counter()
    print(f"Greedy packs: {len(packs)} (time {t1-t0:.3f}s)")

    # 5) build cover instance
    sets, budgets, cover_map = build_cover_instance(G, root, terminals, packs, D_star, k)

    # 6) pmcover variants
    t0 = time.perf_counter()
    half = pmcover_half(sets, budgets, max(0, k - sum(len(p) for p in packs)))
    t1 = time.perf_counter()
    print(f"PMCover half → {len(half)} sets, time {t1-t0:.3f}s")

    t0 = time.perf_counter()
    full = pmcover_continuous(sets, budgets, max(0, k - sum(len(p) for p in packs)), iters=iters, samples=samples)
    t1 = time.perf_counter()
    print(f"PMCover full → {len(full)} sets, time {t1-t0:.3f}s")

    t0 = time.perf_counter()
    lazy = pmcover_lazy(sets, budgets, max(0, k - sum(len(p) for p in packs)))
    t1 = time.perf_counter()
    print(f"PMCover lazy → {len(lazy)} sets, time {t1-t0:.3f}s")

    # 7) stitch & simulate
    t0 = time.perf_counter()
    T = complete(G, root, packs, lazy, cover_map, k)
    rounds = simulate_broadcast_rounds(T, root, terminals)
    t1 = time.perf_counter()
    print(f"Broadcast rounds: {rounds} (time {t1-t0:.3f}s)\n")

if __name__ == "__main__":
    main()
