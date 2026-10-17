
"""Visualization utilities for pathfinding experiments."""

from pathlib import Path
from typing import Optional, Set, Tuple

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

from src.maze import Maze

Position = Tuple[int, int]


def plot_path(
    maze: Maze,
    result: dict,
    output_path: Optional[str] = None,
    title: Optional[str] = None,
) -> None:
    """Plot explored cells and the final path."""

    # 0 = free, 1 = obstacle, 2 = explored, 3 = final path
    explored: Set[Position] = set(result.get("expanded_order", []))
    path: Set[Position] = set(result["path"])

    data = []

    for r, row in enumerate(maze.grid):
        values = []

        for c, cell in enumerate(row):
            position = (r, c)

            if cell == "#":
                values.append(1)
            elif position in path and cell not in {"S", "G"}:
                values.append(3)
            elif position in explored and cell not in {"S", "G"}:
                values.append(2)
            else:
                values.append(0)

        data.append(values)

    cmap = ListedColormap([
        "white",
        "black",
        "lightskyblue",
        "lightgreen",
    ])

    fig, ax = plt.subplots(figsize=(8, 7))
    ax.imshow(data, cmap=cmap, vmin=0, vmax=3)

    ax.set_xticks(range(maze.cols))
    ax.set_yticks(range(maze.rows))
    ax.set_xticks(
        [x - 0.5 for x in range(1, maze.cols)],
        minor=True,
    )
    ax.set_yticks(
        [y - 0.5 for y in range(1, maze.rows)],
        minor=True,
    )

    ax.grid(which="minor", color="gray", linewidth=0.7)
    ax.tick_params(which="both", bottom=False, left=False)

    sr, sc = maze.start
    gr, gc = maze.goal

    ax.scatter(sc, sr, color="blue", marker="o", s=150)
    ax.scatter(gr, gc, color="red", marker="*", s=220)

    route = result["path"]

    if route:
        ax.plot(
            [position[1] for position in route],
            [position[0] for position in route],
            color="green",
            linewidth=2.5,
            marker=".",
            markersize=7,
        )

    heading = title or f"{result['algorithm']} Pathfinding"

    ax.set_title(
        f"{heading}\n"
        f"Success: {result['success']} | "
        f"Path length: {result['path_length']} | "
        f"Expanded nodes: {result['expanded_nodes']} | "
        f"Runtime: {result['runtime_ms']:.4f} ms"
    )

    ax.set_xlabel("Column")
    ax.set_ylabel("Row")

    legend_items = [
        Patch(facecolor="black", label="Obstacle"),
        Patch(facecolor="white", edgecolor="gray", label="Free cell"),
        Patch(facecolor="lightskyblue", label="Explored cell"),
        Patch(facecolor="lightgreen", label="Final path"),
    ]

    ax.legend(
        handles=legend_items,
        loc="upper left",
        bbox_to_anchor=(1.02, 1),
    )

    fig.tight_layout()

    if output_path:
        destination = Path(output_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(destination, dpi=200, bbox_inches="tight")
        print(f"Saved visualization: {destination.resolve()}")

    plt.show()
    plt.close(fig)
