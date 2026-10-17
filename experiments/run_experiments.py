
"""Run reproducible A* and Dijkstra benchmark experiments."""

import sys
from pathlib import Path

import pandas as pd

# Allow running this script directly from the experiments folder.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.maze import Maze
from src.pathfinding import astar, dijkstra
from src.visualization import plot_path


OUTPUT_DIR = PROJECT_ROOT / "results"
FIGURE_DIR = OUTPUT_DIR / "figures"
MAZE_DIR = OUTPUT_DIR / "mazes"

ALGORITHMS = (dijkstra, astar)


def run_benchmarks():
    """Run multiple configurations and export detailed results."""

    OUTPUT_DIR.mkdir(exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    MAZE_DIR.mkdir(parents=True, exist_ok=True)

    configurations = [
        (10, 10, 0.10),
        (10, 10, 0.25),
        (20, 20, 0.10),
        (20, 20, 0.25),
        (30, 30, 0.10),
        (30, 30, 0.25),
        (30, 30, 0.35),
        (50, 50, 0.10),
        (50, 50, 0.25),
        (50, 50, 0.35),
    ]

    repeats = 5
    records = []

    for rows, cols, density in configurations:
        for repetition in range(repeats):
            seed = 20261017 + repetition

            maze = Maze.random_maze(
                rows=rows,
                cols=cols,
                obstacle_density=density,
                seed=seed,
            )

            maze_id = (
                f"{rows}x{cols}_density{density:.2f}"
                f"_seed{seed}"
            )

            maze_file = MAZE_DIR / f"{maze_id}.txt"
            maze_file.write_text(
                "\n".join(maze.grid),
                encoding="utf-8",
            )

            for algorithm in ALGORITHMS:
                result = algorithm(maze)

                walkable_cells = sum(
                    cell != "#"
                    for row in maze.grid
                    for cell in row
                )

                expanded_density = (
                    result["expanded_nodes"] / walkable_cells
                    if walkable_cells
                    else 0.0
                )

                records.append({
                    "maze_id": maze_id,
                    "rows": rows,
                    "cols": cols,
                    "obstacle_density": density,
                    "seed": seed,
                    "algorithm": result["algorithm"],
                    "success": result["success"],
                    "path_length": result["path_length"],
                    "runtime_ms": result["runtime_ms"],
                    "expanded_nodes": result["expanded_nodes"],
                    "walkable_cells": walkable_cells,
                    "expanded_node_density": expanded_density,
                })

                # Save example visualizations for the first seed.
                
                if repetition == 0:
                    algorithm_name = (
                        "astar"
                    if result["algorithm"] == "A*"
                    else "dijkstra"
                    )

                    figure_path = FIGURE_DIR / (
                        f"{maze_id}_{algorithm_name}.png"
                    )

                    plot_path(
                        maze,
                        result,
                        output_path=str(figure_path),
                        title=f"{result['algorithm']} — {maze_id}",
                    )


    results = pd.DataFrame(records)

    detailed_csv = OUTPUT_DIR / "benchmark_results.csv"
    results.to_csv(detailed_csv, index=False)

    summary = (
        results.groupby(
            ["rows", "cols", "obstacle_density", "algorithm"],
            as_index=False,
        )
        .agg(
            trials=("maze_id", "count"),
            success_rate=("success", "mean"),
            mean_path_length=("path_length", "mean"),
            mean_runtime_ms=("runtime_ms", "mean"),
            median_runtime_ms=("runtime_ms", "median"),
            mean_expanded_nodes=("expanded_nodes", "mean"),
            mean_expanded_node_density=("expanded_node_density", "mean"),
        )
    )

    summary["success_rate_percent"] = summary["success_rate"] * 100

    summary_csv = OUTPUT_DIR / "benchmark_summary.csv"
    summary.to_csv(summary_csv, index=False)

    print("\nDetailed benchmark results:")
    print(detailed_csv)

    print("\nBenchmark summary:")
    print(summary.to_string(index=False))

    print("\nSaved summary:")
    print(summary_csv)

    return results, summary


if __name__ == "__main__":
    run_benchmarks()
