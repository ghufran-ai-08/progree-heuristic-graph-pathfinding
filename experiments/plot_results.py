
"""Generate benchmark charts from the experiment CSV files."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

RESULTS_DIR = PROJECT_ROOT / "results"
FIGURES_DIR = RESULTS_DIR / "figures"


def load_results():
    summary_file = RESULTS_DIR / "benchmark_summary.csv"

    if not summary_file.exists():
        raise FileNotFoundError(
            f"Missing {summary_file}. Run the benchmark first."
        )

    df = pd.read_csv(summary_file)

    required = {
        "rows",
        "cols",
        "obstacle_density",
        "algorithm",
        "success_rate",
        "mean_runtime_ms",
        "mean_expanded_nodes",
        "mean_path_length",
    }

    missing = required - set(df.columns)

    if missing:
        raise ValueError(f"Missing CSV columns: {sorted(missing)}")

    return df


def save_chart(fig, filename):
    destination = FIGURES_DIR / filename
    fig.tight_layout()
    fig.savefig(destination, dpi=220, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved chart: {destination}")


def plot_runtime(df):
    fig, ax = plt.subplots(figsize=(10, 6))

    for algorithm in ["A*", "Dijkstra"]:
        subset = df[df["algorithm"] == algorithm].copy()
        subset["grid_size"] = subset["rows"]

        # Each point represents the mean of five trials.
        for density in sorted(subset["obstacle_density"].unique()):
            group = subset[
                subset["obstacle_density"] == density
            ].sort_values("grid_size")

            ax.plot(
                group["grid_size"],
                group["mean_runtime_ms"],
                marker="o",
                label=f"{algorithm}, {density:.0%} obstacles",
            )

    ax.set_title("Mean Runtime by Grid Size and Obstacle Density")
    ax.set_xlabel("Grid width and height")
    ax.set_ylabel("Mean runtime (ms)")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)

    save_chart(fig, "runtime_comparison.png")


def plot_expanded_nodes(df):
    fig, ax = plt.subplots(figsize=(10, 6))

    for algorithm in ["A*", "Dijkstra"]:
        subset = df[df["algorithm"] == algorithm].copy()

        for density in sorted(subset["obstacle_density"].unique()):
            group = subset[
                subset["obstacle_density"] == density
            ].sort_values("rows")

            ax.plot(
                group["rows"],
                group["mean_expanded_nodes"],
                marker="o",
                label=f"{algorithm}, {density:.0%} obstacles",
            )

    ax.set_title("Mean Expanded Nodes by Grid Size")
    ax.set_xlabel("Grid width and height")
    ax.set_ylabel("Mean expanded nodes")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)

    save_chart(fig, "expanded_nodes_comparison.png")


def plot_success_rate(df):
    data = df.copy()
    data["configuration"] = (
        data["rows"].astype(str)
        + "x"
        + data["cols"].astype(str)
        + " / "
        + (data["obstacle_density"] * 100).round().astype(int).astype(str)
        + "%"
    )

    pivot = data.pivot(
        index="configuration",
        columns="algorithm",
        values="success_rate",
    )

    pivot = pivot.sort_index()

    ax = pivot.plot(
        kind="bar",
        figsize=(12, 6),
        ylim=(0, 1.05),
        width=0.8,
    )

    ax.set_title("Route-Finding Success Rate")
    ax.set_xlabel("Maze size / obstacle density")
    ax.set_ylabel("Success rate")
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(["0%", "20%", "40%", "60%", "80%", "100%"])
    ax.grid(axis="y", alpha=0.3)
    ax.legend(title="Algorithm")
    plt.xticks(rotation=35, ha="right")

    save_chart(ax.figure, "success_rate_comparison.png")


def plot_path_length(df):
    fig, ax = plt.subplots(figsize=(10, 6))

    for algorithm in ["A*", "Dijkstra"]:
        subset = df[df["algorithm"] == algorithm].copy()

        # Unsolvable trials have no path length and are excluded.
        for density in sorted(subset["obstacle_density"].unique()):
            group = subset[
                subset["obstacle_density"] == density
            ].sort_values("rows")

            ax.plot(
                group["rows"],
                group["mean_path_length"],
                marker="o",
                label=f"{algorithm}, {density:.0%} obstacles",
            )

    ax.set_title("Mean Shortest-Path Length for Solvable Mazes")
    ax.set_xlabel("Grid width and height")
    ax.set_ylabel("Mean path length (moves)")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)

    save_chart(fig, "path_length_comparison.png")


def main():
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    df = load_results()

    plot_runtime(df)
    plot_expanded_nodes(df)
    plot_success_rate(df)
    plot_path_length(df)

    print("\nAll benchmark charts generated successfully.")


if __name__ == "__main__":
    main()
