
# Heuristic Graph Pathfinding Agent

An AI search project implementing **A\*** and **Dijkstra's algorithm** from scratch to solve grid-based pathfinding problems. The project includes maze generation, path visualization, automated testing, reproducible benchmarking, and performance analysis.

## Features

- A* search with Manhattan-distance heuristic
- Dijkstra's shortest-path search
- Four-directional grid movement and obstacle avoidance
- Path reconstruction and unreachable-goal handling
- Random maze generation using reproducible seeds
- Visualization of explored cells and final paths
- Benchmarking across multiple grid sizes and obstacle densities
- CSV export and performance charts
- Automated correctness and data-validation tests

## Technology Stack

- Python 3.10
- NumPy
- Matplotlib
- pandas
- Python standard library: `heapq`, `time`, `random`, and `unittest`

## Project Structure

```text
.
├── src/
│   ├── maze.py
│   ├── pathfinding.py
│   ├── visualization.py
│   └── __init__.py
├── tests/
│   └── test_pathfinding.py
├── experiments/
│   ├── run_experiments.py
│   ├── plot_results.py
│   └── validate_results.py
├── results/
│   ├── figures/
│   ├── mazes/
│   ├── benchmark_results.csv
│   └── benchmark_summary.csv
├── docs/
│   └── PROJECT_REPORT.md
├── requirements.txt
└── README.md
```

## Setup

Create and activate a virtual environment from the project root.

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run Tests

```powershell
python -m unittest discover -s tests -v
```

## Run the Benchmark

```powershell
python experiments/run_experiments.py
```

The benchmark evaluates both algorithms on the same generated mazes and saves detailed and aggregated measurements in the `results/` directory.

## Generate Charts

```powershell
python experiments/plot_results.py
```

The generated charts compare runtime, expanded nodes, success rate, and path length.

## Validate Results

```powershell
python experiments/validate_results.py
```

The validation script checks experiment completeness, metric validity, agreement on route existence, and equal path lengths for successful searches.

## Experimental Summary

The initial experiment includes:

- 50 unique random mazes
- 100 algorithm runs
- Grid sizes of 10×10, 20×20, 30×30, and 50×50
- Obstacle densities of 10%, 25%, and 35%, depending on grid size
- Five random seeds per configuration

Both algorithms agreed on route existence and shortest-path length in the generated experiments. A* generally expanded fewer nodes, although runtime advantages varied by configuration.

For full methodology, measurements, limitations, and conclusions, see `docs/PROJECT_REPORT.md`.

## Limitations

- Each configuration uses five random seeds.
- Random obstacle placement does not guarantee a solvable maze.
- Runtime can vary with machine load and system conditions.
- The current implementation uses four-directional movement with uniform edge costs.

## Future Improvements

- Increase the number of benchmark repetitions.
- Report timing variability and confidence intervals.
- Add larger mazes and weighted graph search.
- Explore alternative heuristics and maze-generation methods.

## Author

### M.Ghufran

Developed as an AI search and pathfinding internship project.
