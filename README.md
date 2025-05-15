# Directed k-MTM Multicast

Python implementation & evaluation of a $\tilde O(\sqrt{k})$‐additive approximation for the directed $k$-MTM problem.

---

## Quick Start

All of the latest code and demo live in **`milestones/Milestone4/`**.

1. **Clone** and enter the repository:

   ```bash
   git clone <your-repo-url>
   cd Algo-Project
   ```

2. **Navigate** to the final milestone:

   ```bash
   cd milestones/Milestone4
   ```

3. **Run the demo**:

   ```bash
   cd demo
   python -m demo.demo \
     --graph ER --n 500 --p 0.005 \
     --t_ratio 0.2 --k_ratio 0.6 \
     --D_star 3 --iters 20 --samples 20
   ```

   This command generates a 500-node Erdős–Rényi graph, picks 100 terminals, sets $k=0.6\times100$, runs depth-3 greedy packing, then all three PMCover routines, stitches the final tree, and simulates the telephone rounds.

4. **Run tests** (from the Milestone4 root):

   ```bash
   pytest --maxfail=1 -q
   ```

   All unit tests and a smoke integration test should pass.

5. **Generate benchmarks**:

   ```bash
   cd ../experiments
   python -m run_synthetic_benchmarks
   ```

   The `plots/` folder will be populated with coverage and runtime graphs.

---

## Demo Video

A recorded walkthrough and live demo are available at:
[[https://habibuniversity-my.sharepoint.com/\:v:/g/personal/ha07194\_st\_habib\_edu\_pk/EWt9SubaxnZKubO3Uha6QGkB8BkNfdeWag8V5KpSQilHvQ?e=RnlxP0](https://habibuniversitymy.sharepoint.com/:v:/g/personal/ha07194_st_habib_edu_pk/EWt9SubaxnZKubO3Uha6QGkB8BkNfdeWag8V5KpSQilHvQ?e=RnlxP0)
](https://habibuniversity-my.sharepoint.com/:v:/g/personal/ha07194_st_habib_edu_pk/EWt9SubaxnZKubO3Uha6QGkB8BkNfdeWag8V5KpSQilHvQ?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=RnlxP0)
---

## Milestones

* **Milestone1/**: Proposal & paper selection
* **Milestone2/**: Technical summary & breakdown
* **Milestone3/**: Progress report & intermediate code
* **Milestone4/**: Final code, tests, report, and slides

Refer to each folder for the state at that checkpoint.
