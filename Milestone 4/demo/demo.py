#!/usr/bin/env python3
"""
End-to-end demo for directed k-MTM multicast pipeline.
Usage example:
  python -m demo.demo \
    --graph ER --n 500 --p 0.005 \
    --t_ratio 0.2 --k_ratio 0.6 \
    --D_star 3 --iters 20 --samples 20
"""
import argparse
import time
import math
import random
from collections import deque

import networkx as nx

from src.graph_loader import generate_directed_ER, generate_directed_clique
from src.greedy_packing import find_greedy_packing, bfs_subtree_nodes
from src.pmcover import pmcover_half
from src.pmcover_continuous import pmcover_continuous
from src.pmcover_lazy import pmcover_lazy
from src.complete import complete
from src.simulator import simulate_broadcast_rounds


def build_cover_instance(
    G: nx.DiGraph,
    root: int,
    terminals: set,
    packs: list,
    D_star: int,
    k: int
):
    """
    Constructs the partition-matroid cover instance after greedy packing.
    A = {root} ∪ all terminals covered by packs.
    C = V \ A.
    For each edge a->c with a in A, c in C, define the set of terminals
    reachable from c within D_star hops (restricted to C).
    Budgets[a] is set to ceil(sqrt(k)) for all a in A.
    Returns: sets, budgets, cover_map
      - sets: Dict[(a,c), Set[terminal]]
      - budgets: Dict[a, int]
      - cover_map: Dict[c, List[terminal]] for complete()
    """
    # Determine A and C
    covered_by_packs = set().union(*packs) if packs else set()
    A = {root} | covered_by_packs
    C = set(G.nodes()) - A

    # Budgets: use rho = ceil(sqrt(k)) as degree bound
    rho = math.ceil(math.sqrt(k))
    budgets = {a: rho for a in A}

    sets = {}
    cover_map = {}

    # For each a->c edge crossing A->C, compute coverage
    for a in A:
        for c in G.successors(a):
            if c not in C:
                continue
            # BFS from c restricted to C up to depth D_star
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


def parse_args():
    p = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    p.add_argument("--graph", choices=["ER", "clique"], required=True,
                   help="Graph type")
    p.add_argument("--n",     type=int,   required=True,
                   help="Number of nodes")
    p.add_argument("--p",     type=float, default=0.01,
                   help="ER edge probability")
    p.add_argument("--t_ratio", type=float, default=0.2,
                   help="Fraction of nodes chosen as terminals")
    p.add_argument("--k_ratio", type=float, default=0.5,
                   help="Fraction of terminals to inform (k/t)")
    p.add_argument("--D_star",  type=int,   default=3,
                   help="Depth bound for greedy packing / cover BFS")
    p.add_argument("--iters",   type=int,   default=20,
                   help="Iterations for continuous-greedy")
    p.add_argument("--samples", type=int,   default=20,
                   help="Samples per iteration for continuous-greedy")
    return p.parse_args()


def main():
    args = parse_args()

    # 1. Generate graph
    if args.graph == "ER":
        G = generate_directed_ER(args.n, args.p, seed=42)
    else:
        G = generate_directed_clique(args.n)

    root = 0
    nodes = list(G.nodes())

    # 2. Sample terminals
    t = max(1, int(args.t_ratio * args.n))
    terminals = set(random.sample(nodes, t))
    if root in terminals:
        terminals.remove(root)
    t = len(terminals)

    # 3. Compute k
    k = max(1, int(args.k_ratio * t))

    print(f"\nGraph: {args.graph}(n={args.n}, p={args.p}), "
          f"terminals={t}, k={k}, D*={args.D_star}\n")

    # 4. Greedy Packing
    start = time.perf_counter()
    packs = find_greedy_packing(G, root, terminals, k, args.D_star)
    gp_time = time.perf_counter() - start
    covered = set().union(*packs) if packs else set()
    print(f"Greedy packing → {len(packs)} packs, "
          f"covered {len(covered)}/{k} in {gp_time:.3f}s")

    # 5. Determine remaining
    k_rem = max(0, k - len(covered))

    # 6. Build cover instance
    sets, budgets, cover_map = build_cover_instance(
        G, root, terminals, packs, args.D_star, k
    )

    # 7. PMCover variants
    # 7a. half
    start = time.perf_counter()
    half_sel = pmcover_half(sets, budgets, k_rem)
    half_time = time.perf_counter() - start
    half_cov = len(set().union(*(sets[key] for key in half_sel)))
    print(f"PMCover half → covered {half_cov}/{k_rem} in {half_time:.3f}s")

    # 7b. full (continuous)
    start = time.perf_counter()
    full_sel = pmcover_continuous(sets, budgets, k_rem,
                                  iters=args.iters,
                                  samples=args.samples)
    full_time = time.perf_counter() - start
    full_cov = len(set().union(*(sets[key] for key in full_sel)))
    print(f"PMCover full → covered {full_cov}/{k_rem} in {full_time:.3f}s")

    # 7c. lazy
    start = time.perf_counter()
    lazy_sel = pmcover_lazy(sets, budgets, k_rem)
    lazy_time = time.perf_counter() - start
    lazy_cov = len(set().union(*(sets[key] for key in lazy_sel)))
    print(f"PMCover lazy → covered {lazy_cov}/{k_rem} in {lazy_time:.3f}s\n")

    # 8. Stitch and simulate
    start = time.perf_counter()
    T = complete(G, root, packs, lazy_sel, cover_map, k)
    rounds = simulate_broadcast_rounds(T, root, terminals)
    sim_time = time.perf_counter() - start
    print(f"Broadcast rounds → {rounds} rounds in {sim_time:.3f}s\n")


if __name__ == "__main__":
    main()
