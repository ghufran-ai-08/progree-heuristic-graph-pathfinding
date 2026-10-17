
"""Validate benchmark CSV data and algorithm consistency."""

from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = PROJECT_ROOT / "results"


def main():
    detailed_file = RESULTS_DIR / "benchmark_results.csv"
    summary_file = RESULTS_DIR / "benchmark_summary.csv"

    assert detailed_file.exists(), "Detailed benchmark CSV is missing."
    assert summary_file.exists(), "Benchmark summary CSV is missing."

    df = pd.read_csv(detailed_file)
    summary = pd.read_csv(summary_file)

    required = {
        "maze_id",
        "algorithm",
        "success",
        "path_length",
        "runtime_ms",
        "expanded_nodes",
        "walkable_cells",
        "expanded_node_density",
    }

    missing = required - set(df.columns)
    assert not missing, f"Missing columns: {sorted(missing)}"

    # Expected experiment size: 50 mazes x 2 algorithms.
    assert len(df) == 100, f"Expected 100 runs; found {len(df)}."
    assert df["maze_id"].nunique() == 50
    assert set(df["algorithm"]) == {"A*", "Dijkstra"}

    assert df["runtime_ms"].notna().all()
    assert (df["runtime_ms"] >= 0).all()
    assert (df["expanded_nodes"] >= 0).all()
    assert (df["walkable_cells"] > 0).all()

    assert df["expanded_node_density"].between(0, 1).all()

    # Failed searches should not have a path length.
    failed = df[~df["success"]]
    assert failed["path_length"].isna().all()

    # Every maze must have one result from each algorithm.
    counts = df.groupby("maze_id")["algorithm"].nunique()
    assert (counts == 2).all()

    paired = df.pivot(
        index="maze_id",
        columns="algorithm",
        values="success",
    )

    assert (
        paired["A*"] == paired["Dijkstra"]
    ).all(), "Algorithms disagree on whether a path exists."

    # Both optimal algorithms should return equal path lengths
    # whenever a route exists.
    successful = df[df["success"]].pivot(
        index="maze_id",
        columns="algorithm",
        values="path_length",
    )

    assert (
        successful["A*"] == successful["Dijkstra"]
    ).all(), "Algorithms returned different path lengths."

    print("BENCHMARK VALIDATION PASSED")
    print(f"Individual algorithm runs: {len(df)}")
    print(f"Unique mazes: {df['maze_id'].nunique()}")
    print(f"Summary rows: {len(summary)}")
    print(f"Successful runs: {int(df['success'].sum())}/100")
    print(f"Unsuccessful runs: {int((~df['success']).sum())}/100")
    print("Success decisions agree between algorithms.")
    print("Shortest-path lengths agree for successful mazes.")
    print("Runtime and expanded-node density checks passed.")


if __name__ == "__main__":
    main()
