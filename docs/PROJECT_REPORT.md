
# Heuristic Graph Pathfinding Agent: A* vs. Dijkstra

## 1. Abstract

This project implements two classical graph-search algorithms, A* and Dijkstra's algorithm, from scratch to solve grid-based pathfinding problems. The implementation supports four-directional movement, obstacle avoidance, shortest-path reconstruction, unreachable-goal detection, and performance measurement.

The algorithms were evaluated on randomly generated mazes of sizes 10×10, 20×20, 30×30, and 50×50, with obstacle densities ranging from 10% to 35%. Experiments measured path length, runtime, expanded nodes, expanded-node density, and route-finding success rate.

Across 100 algorithm runs, both algorithms agreed on route existence and produced equal shortest-path lengths whenever a route existed. A* generally expanded fewer nodes, although its runtime advantage varied by configuration.

## 2. Objectives

The objectives were to:

- Implement A* and Dijkstra's algorithm without relying on a pathfinding library.
- Represent mazes as rectangular grids with obstacles, a start, and a goal.
- Reconstruct optimal paths and handle unreachable goals.
- Visualize explored cells and final paths.
- Compare search performance across different maze sizes and obstacle densities.
- Export reproducible experimental results and performance charts.

## 3. Methodology

### 3.1 Maze representation

Each maze is represented as a rectangular grid:

- `S`: starting cell
- `G`: goal cell
- `#`: obstacle
- `.`: traversable cell

Movement is restricted to up, down, left, and right. Diagonal movement is not permitted, and every move has a cost of one.

### 3.2 Dijkstra's algorithm

Dijkstra's algorithm uses a priority queue ordered by the accumulated path cost. It expands the lowest-cost frontier state and updates neighboring states when a lower-cost route is discovered.

### 3.3 A* algorithm

A* orders frontier states using the sum of the accumulated path cost and a heuristic estimate of the remaining cost.

The Manhattan-distance heuristic is:

h(n) = |row(n) - row(goal)| + |col(n) - col(goal)|

For four-directional movement with unit edge costs, this heuristic is admissible and consistent. A* therefore finds an optimal path when a route exists.

### 3.4 Experimental configuration

The benchmark used ten configurations:

- Grid sizes: 10×10, 20×20, 30×30, and 50×50.
- Obstacle densities: 10%, 25%, and 35%, where applicable.
- Five random seeds per configuration.
- Two algorithms evaluated on each generated maze.

The random seeds began at 20261017. Each algorithm was evaluated on the same maze for a fair comparison.

This produced 50 unique mazes and 100 individual algorithm runs.

### 3.5 Performance metrics

**Path length:** Number of moves in the returned path.

**Runtime:** Measured execution time in milliseconds using Python's high-resolution performance timer.

**Expanded nodes:** Number of search states removed from the priority queue and processed, excluding outdated queue entries.

**Expanded-node density:** Expanded nodes divided by the number of walkable cells.

**Success rate:** Proportion of trials in which a route was found.

## 4. Results

### 4.1 Overall validation

The benchmark produced the following results:

- Individual algorithm runs: 100.
- Unique maze configurations generated across seeds: 50.
- Successful algorithm runs: 72 out of 100 (72%).
- Unsuccessful algorithm runs: 28 out of 100 (28%).
- Automated pathfinding tests: 7 passed.
- Agreement on route existence: 100%.
- Agreement on path length for solvable mazes: 100%.

Because both algorithms were tested on the same mazes, the 72 successful runs correspond to 36 solvable mazes out of 50. Fourteen mazes were unsolvable.

### 4.2 Representative performance results

| Grid | Obstacles | Algorithm | Mean runtime (ms) | Mean expanded nodes | Mean path length |
|---|---:|---|---:|---:|---:|
| 10×10 | 10% | A* | 0.913 | 76.0 | 18 |
| 10×10 | 10% | Dijkstra | 0.935 | 89.4 | 18 |
| 20×20 | 10% | A* | 7.330 | 308.6 | 38 |
| 20×20 | 10% | Dijkstra | 9.389 | 358.0 | 38 |
| 50×50 | 10% | A* | 25.407 | 1953.8 | 98 |
| 50×50 | 10% | Dijkstra | 32.212 | 2244.4 | 98 |
| 50×50 | 25% | A* | 11.361 | 775.6 | 98.5 |
| 50×50 | 25% | Dijkstra | 13.110 | 1493.2 | 98.5 |

The path lengths in this table are averages across successful trials. Unsuccessful trials have no path length.

### 4.3 Node expansion

A* expanded fewer nodes than Dijkstra in the reported configurations. For example, on the 50×50 mazes with 10% obstacles, A* expanded an average of 1,953.8 nodes compared with 2,244.4 for Dijkstra.

At 50×50 with 25% obstacles, A* expanded an average of 775.6 nodes compared with 1,493.2 for Dijkstra.

These results are consistent with the benefit of heuristic guidance: A* prioritizes states that appear closer to the goal, while Dijkstra explores according to accumulated path cost alone.

### 4.4 Runtime

A* had a lower mean runtime in several configurations, including the two 50×50 configurations above. However, runtime differences were not uniform across all experiments.

Small timing measurements can be affected by operating-system scheduling, interpreter overhead, and other background activity. The experiment should therefore be interpreted as an initial comparison rather than a definitive performance ranking.

### 4.5 Effect of obstacles

Obstacle density affected both route availability and search behavior.

At 30×30 with 35% obstacles, none of the five generated mazes had a valid route. At 50×50 with 35% obstacles, two of the five mazes were solvable.

An unsolvable maze may require fewer expansions than a solvable maze because the search terminates after exhausting the reachable region. Lower runtime does not necessarily indicate a better search result.

## 5. Visualizations

The project generates visualizations of:

- Maze obstacles and traversable cells.
- Search-explored cells.
- Final paths.
- Runtime, path length, and expanded-node information.
- Runtime comparisons between algorithms.
- Expanded-node comparisons.
- Route-finding success rates.
- Path lengths across maze configurations.

The generated figures are saved in `results/figures/`.

## 6. Software testing and reproducibility

Seven automated tests verify optimal path length, valid neighbor transitions, unreachable-goal handling, adjacent start and goal cells, and invalid maze inputs.

The benchmark validator also checks CSV completeness, nonnegative runtimes, expanded-node density bounds, agreement on route existence, and equal path lengths for successful searches.

To reproduce the experiments from the project root:

```powershell
python -m unittest discover -s tests -v
python experiments/run_experiments.py
python experiments/plot_results.py
python experiments/validate_results.py
```

The benchmark uses fixed random seeds. Runtime measurements can still vary between executions.

## 7. Limitations

1. Each configuration uses five random seeds, which is a relatively small sample.
2. Random obstacle placement does not guarantee a route between the start and goal.
3. Runtime measurements are sensitive to machine load and interpreter overhead.
4. The current experiment evaluates four-directional, unit-cost grid movement rather than weighted or diagonal pathfinding.
5. The experiment does not evaluate dynamic obstacles or changes to the maze during search.

Future improvements could include more random seeds, repeated timing measurements, confidence intervals, larger grids, and maze generation methods that guarantee connectivity.

## 8. Conclusion

The project successfully implements A* and Dijkstra's algorithm from scratch and evaluates them on reproducible grid-based pathfinding experiments.

Both algorithms produced consistent route-existence decisions and equal shortest-path lengths for solvable mazes. A* generally reduced the number of expanded nodes, demonstrating the value of the Manhattan-distance heuristic. Runtime results varied by maze configuration, emphasizing the importance of repeated measurements and careful interpretation.

The project provides a foundation for further work in heuristic search, graph algorithms, experimental evaluation, and visualization.

## 9. Project artifacts

- `src/maze.py`: Maze representation and random maze generation.
- `src/pathfinding.py`: A* and Dijkstra implementations.
- `src/visualization.py`: Maze and search-result visualization.
- `tests/test_pathfinding.py`: Automated tests.
- `experiments/run_experiments.py`: Benchmark execution.
- `experiments/plot_results.py`: Chart generation.
- `experiments/validate_results.py`: Benchmark validation.
- `results/benchmark_results.csv`: Individual-run measurements.
- `results/benchmark_summary.csv`: Aggregated metrics.
- `results/figures/`: Generated visualizations and performance charts.
