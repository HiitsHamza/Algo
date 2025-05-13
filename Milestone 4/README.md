# Directed k-MTM Approximation Algorithm

This project implements and benchmarks a directed k-MTM (Minimum Time Telephone Multicast) approximation algorithm. The algorithm finds efficient multicast trees in directed graphs to broadcast information from a root node to a set of terminal nodes.

## Overview

The implementation follows a multi-stage approach:
1. Greedy packing to find disjoint paths
2. Matroid-constrained set cover for remaining terminals
3. Tree stitching to create the final multicast structure
4. Broadcast simulation to measure rounds needed

Three different matroid-constrained set cover implementations are provided:
- Half-approximation greedy algorithm
- Continuous-greedy approximation
- Lazy-greedy implementation (fastest in practice)

## Installation

### Requirements

- Python 3.6+
- NetworkX
- Matplotlib
- pytest

### Setup

```bash
# Clone this repository
git clone <repository-url>
cd ./Milestone4

# Install dependencies
pip install -r requirements.txt
```

## Running the Demo

The demo CLI provides an interactive way to test the algorithm on different graph types:

```bash
# Basic usage with required arguments
python -m demo.demo --graph ER --n 200

# Specify more parameters
python -m demo.demo --graph ER --n 200 --p 0.05 --t_ratio 0.2 --k_ratio 0.5 --D_star 3 --iters 20 --samples 20
```

Command-line arguments:
- `--graph`: 'ER' (Erdős-Rényi) or 'clique'
- `--n`: Number of nodes
- `--p`: Edge probability (for ER graphs)
- `--t_ratio`: Fraction of nodes to use as terminals
- `--k_ratio`: Fraction of terminals to cover
- `--D_star`: Maximum path length
- `--iters`: Iterations for continuous-greedy algorithm
- `--samples`: Samples per iteration for continuous-greedy

## Generating Benchmarks and Plots

To generate the performance comparison plots:

```bash
# Run the synthetic benchmarks
python -m experiments.run_synthetic_benchmarks

# Run a simpler integration test on a clique
python -m experiments.run_integration
```

The benchmark will:
1. Generate Erdős-Rényi graphs of various sizes
2. Run all algorithm variants (greedy packing, half-approx, continuous, lazy)
3. Measure coverage and runtime for each
4. Generate plots in the `plots/` directory

## Generated Plots

The benchmark generates four plots:
- `coverage_comparison.png`: Shows coverage achieved by each algorithm vs graph size
- `runtime_comparison.png`: Compares runtime of all algorithms (log scale)
- `runtime_scaling.png`: Shows how runtime scales with graph size (log-log)
- `coverage_curve.png`: Coverage vs k_ratio for a fixed graph size
- `runtime_comparison_small.png`: Focused view of half-approx and lazy greedy runtimes

## Project Structure

```
.
├── src/                    # Core algorithm modules
│   ├── graph_loader.py     # Graph generation
│   ├── greedy_packing.py   # Disjoint path packing
│   ├── pmcover.py          # Half-approximation matroid cover
│   ├── pmcover_continuous.py # Continuous-greedy implementation
│   ├── pmcover_lazy.py     # Lazy-greedy implementation
│   ├── complete.py         # Tree stitching
│   └── simulator.py        # Broadcast simulation
├── tests/                  # Unit tests for each module
├── demo/                   # Interactive CLI
│   └── demo.py             # Demo entrypoint
├── experiments/            # Benchmarking scripts
│   ├── run_integration.py  # End-to-end test
│   └── run_synthetic_benchmarks.py # Parameter sweeps and plotting
├── plots/                  # Generated plots
└── README.md               # This file
```

## Troubleshooting

- **RecursionError**: For large graphs, the simulator may hit Python's recursion limit. We've implemented an iterative version to avoid this.
- **No path between nodes**: If the graph is not strongly connected, some paths may not exist. Error handling is in place to skip unreachable nodes.
- **Slow simulation**: For graphs larger than n=400, depth computation may time out. Adjust the timeout parameter in `run_synthetic_benchmarks.py` if needed.

## Running Tests

To run the test suite:

```bash
# Run all tests
python -m pytest tests/

# Run specific tests
python -m pytest tests/test_greedy_packing.py
```
