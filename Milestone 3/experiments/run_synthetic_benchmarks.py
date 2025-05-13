import matplotlib.pyplot as plt
import networkx as nx
import time
import math

from src.graph_loader import generate_directed_ER
from src.greedy_packing import find_greedy_packing
from src.pmcover import pmcover
from src.complete import complete
from src.simulator import simulate_broadcast_rounds

def plot_coverage_curve(n=1000, t_ratio=0.1, k_ratio=0.5, p=0.05):
    G = generate_directed_ER(n, p, seed=42)
    root = 0
    terminals = set(range(1, int(n * t_ratio) + 1))
    k = int(len(terminals) * k_ratio)
    D_star = int(math.log2(n))

    # Build tree schedule (skip pmcover for simplicity)
    packs = find_greedy_packing(G, root, terminals, k, D_star)
    cover_edges = []
    T = complete(G, root, packs, cover_edges, k)

    # Simulate per-round coverage
    informed = {root}
    to_cover = set(terminals)
    coverage = [len(informed & terminals)]
    children = {u: list(T.successors(u)) for u in T.nodes()}

    while to_cover:
        new_inf = set()
        for u in list(informed):
            for v in children.get(u, []):
                if v not in informed:
                    new_inf.add(v)
                    break
        if not new_inf:
            break
        informed |= new_inf
        to_cover -= new_inf
        coverage.append(len(informed & terminals))

    plt.figure()
    plt.plot(range(len(coverage)), coverage, marker='o')
    plt.xlabel("Round")
    plt.ylabel("Terminals Informed")
    plt.title(f"Coverage Curve (n={n}, t={len(terminals)}, k={k})")
    plt.savefig("plots/coverage_curve.png")
    plt.close()

def plot_poise_scatter(n=1000, t_ratio=0.1, p=0.05, k_factors=None):
    if k_factors is None:
        k_factors = [0.2, 0.4, 0.6, 0.8]
    sqrt_k = []
    poise_diff = []

    G = generate_directed_ER(n, p, seed=123)
    root = 0
    terminals = set(range(1, int(n * t_ratio) + 1))
    D_star = int(math.log2(n))

    for f in k_factors:
        k = int(len(terminals) * f)
        packs = find_greedy_packing(G, root, terminals, k, D_star)
        cover_edges = []
        T = complete(G, root, packs, cover_edges, k)

        # Compute out-degree and height
        out_deg = max(dict(T.out_degree()).values())
        depth = {root: 0}
        queue = [root]
        while queue:
            u = queue.pop(0)
            for v in T.successors(u):
                depth[v] = depth[u] + 1
                queue.append(v)
        height = max(depth.values())

        sqrt_k.append(math.sqrt(k))
        poise_diff.append((out_deg + height) - D_star)

    plt.figure()
    plt.scatter(sqrt_k, poise_diff)
    plt.xlabel("sqrt(k)")
    plt.ylabel("Poise − D*")
    plt.title(f"Poise Scatter (n={n}, t={int(n*t_ratio)})")
    plt.savefig("plots/poise_scatter.png")
    plt.close()

def plot_runtime_scaling(t_ratio=0.1, k_ratio=0.5, p=0.05):
    ns = [100, 500, 1000, 2000, 5000]
    times = []

    for n in ns:
        G = generate_directed_ER(n, p, seed=999)
        root = 0
        terminals = set(range(1, int(n * t_ratio) + 1))
        k = int(len(terminals) * k_ratio)
        D_star = int(math.log2(n))

        start = time.time()
        packs = find_greedy_packing(G, root, terminals, k, D_star)
        cover_edges = []
        T = complete(G, root, packs, cover_edges, k)
        simulate_broadcast_rounds(T, root, terminals)
        times.append(time.time() - start)

    plt.figure()
    plt.loglog(ns, times, marker='o')
    plt.xlabel("n (nodes)")
    plt.ylabel("Runtime (seconds)")
    plt.title("Runtime Scaling (end-to-end)")
    plt.savefig("plots/runtime_scaling.png")
    plt.close()

if __name__ == "__main__":
    plot_coverage_curve()
    plot_poise_scatter()
    plot_runtime_scaling()

