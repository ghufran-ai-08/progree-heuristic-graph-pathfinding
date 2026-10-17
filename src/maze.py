
"""Maze representation for the pathfinding agent."""


import random

from typing import List, Tuple

Position = Tuple[int, int]


class Maze:
    """A rectangular grid maze with four-directional movement."""

    MOVES = (
        (-1, 0),  # Up
        (1, 0),   # Down
        (0, -1),  # Left
        (0, 1),   # Right
    )

    def __init__(self, grid: List[str]) -> None:
        if not grid:
            raise ValueError("Maze cannot be empty.")

        if any(not row for row in grid):
            raise ValueError("Maze rows cannot be empty.")

        self.grid = [row.strip() for row in grid]
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])

        if any(len(row) != self.cols for row in self.grid):
            raise ValueError("All maze rows must have equal length.")

        allowed = {"S", "G", ".", "#"}

        for row in self.grid:
            invalid = set(row) - allowed
            if invalid:
                raise ValueError(
                    f"Invalid maze symbols: {invalid}"
                )

        starts = [
            (r, c)
            for r, row in enumerate(self.grid)
            for c, cell in enumerate(row)
            if cell == "S"
        ]

        goals = [
            (r, c)
            for r, row in enumerate(self.grid)
            for c, cell in enumerate(row)
            if cell == "G"
        ]

        if len(starts) != 1:
            raise ValueError("Maze must contain exactly one S.")

        if len(goals) != 1:
            raise ValueError("Maze must contain exactly one G.")

        self.start = starts[0]
        self.goal = goals[0]

    def in_bounds(self, position: Position) -> bool:
        """Return whether a position is inside the grid."""
        row, col = position

        return (
            0 <= row < self.rows
            and 0 <= col < self.cols
        )

    def is_walkable(self, position: Position) -> bool:
        """Return whether a position is not a wall."""
        if not self.in_bounds(position):
            return False

        row, col = position
        return self.grid[row][col] != "#"

    def neighbors(self, position: Position) -> List[Position]:
        """Return all walkable four-directional neighbors."""
        row, col = position
        result = []

        for dr, dc in self.MOVES:
            neighbor = (row + dr, col + dc)

            if self.is_walkable(neighbor):
                result.append(neighbor)

        return result

    def display(self) -> None:
        """Print the maze in the terminal."""
        for row in self.grid:
            print(" ".join(row))

    
    @classmethod
    def random_maze(
        cls,
        rows: int,
        cols: int,
        obstacle_density: float,
        seed: int,
    ) -> "Maze":
        """Generate a reproducible random maze."""

        if rows < 2 or cols < 2:
            raise ValueError("Maze dimensions must be at least 2 x 2.")

        if not 0 <= obstacle_density < 1:
            raise ValueError("Obstacle density must be in [0, 1).")

        rng = random.Random(seed)
        grid = []

        for r in range(rows):
            row = []

            for c in range(cols):
                if rng.random() < obstacle_density:
                    row.append("#")
                else:
                    row.append(".")

            grid.append(row)

        # Guarantee valid, walkable start and goal cells.
        grid[0][0] = "S"
        grid[rows - 1][cols - 1] = "G"

        return cls(["".join(row) for row in grid])
