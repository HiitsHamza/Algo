# Telephone k-Multicast Problem (Directed Graphs)

This repository contains the implementation of the directed solution for the Telephone k-Multicast Problem, as described in the paper “[The Telephone k-Multicast Problem](https://arxiv.org/pdf/2410.01048)” (arXiv:2410.01048, APPROX 2024). This project is part of a course final project at Habib University, developed by Hamza Abdullah (School ID: ha07194).

---

## Overview

In the Telephone Model, a message originating at a root node must be spread to a set of terminal nodes in as few rounds as possible—each informed node can call exactly one neighbor per round. This project focuses on the **k-multicast variant**, where the goal is to inform any **\(k\)** out of **\(t\)** terminals efficiently.

Our implementation for directed graphs follows the paper’s approach:
- **Low-Poise Tree Construction:** We build a multicast tree minimizing the “poise” (defined as tree height plus maximum node degree).
- **Greedy Decomposition:** The algorithm iteratively finds disjoint “good” trees (each covering approximately \(\sqrt{k}\) terminals) and connects them via shortest paths to achieve an additive \(\tilde{O}(k^{1/2})\) approximation.
- **Set Cover with Matroid Constraints:** When the initial greedy phase does not cover \(k\) terminals, the remaining coverage problem is formulated as a set cover problem under partition matroid constraints, using submodular maximization techniques.

We also compare our approach with classical shortest-path algorithms (Bellman–Ford and Dijkstra) adapted to the multicast setting.
