
"""Pathfinding algorithms: A* and Dijkstra's algorithm."""

import heapq
import time
from typing import Dict, List, Optional, Tuple

from src.maze import Maze

Position = Tuple[int, int]


def manhattan_distance(a: Position, b: Position) -> int:
    """Heuristic for four-directional grid movement."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def reconstruct_path(
    came_from: Dict[Position, Position],
    start: Position,
    goal: Position,
) -> List[Position]:
    """Reconstruct a path from start to goal."""
    if start == goal:
        return [start]

    if goal not in came_from:
        return []

    path = [goal]
    current = goal

    while current != start:
        current = came_from[current]
        path.append(current)

    path.reverse()
    return path


def dijkstra(maze: Maze) -> dict:
    """Find a shortest path using Dijkstra's algorithm."""
    start_time = time.perf_counter()

    start = maze.start
    goal = maze.goal

    frontier = [(0, start)]
    came_from: Dict[Position, Position] = {}
    cost_so_far: Dict[Position, int] = {start: 0}
    expanded_nodes = 0
    expanded_order = [] 

    while frontier:
        current_cost, current = heapq.heappop(frontier)

        # Ignore outdated queue entries.
        if current_cost != cost_so_far.get(current):
            continue

        expanded_nodes += 1
        expanded_order.append(current)

        if current == goal:
            break

        for neighbor in maze.neighbors(current):
            new_cost = current_cost + 1

            if new_cost < cost_so_far.get(neighbor, float("inf")):
                cost_so_far[neighbor] = new_cost
                came_from[neighbor] = current
                heapq.heappush(frontier, (new_cost, neighbor))

    path = reconstruct_path(came_from, start, goal)
    runtime_ms = (time.perf_counter() - start_time) * 1000

    return {
        "algorithm": "Dijkstra",
        "path": path,
        "path_length": len(path) - 1 if path else None,
        "runtime_ms": runtime_ms,
        "expanded_nodes": expanded_nodes,
        "expanded_order": expanded_order,
        "success": bool(path),
    }


def astar(maze: Maze) -> dict:
    """Find a shortest path using A* and Manhattan distance."""
    start_time = time.perf_counter()

    start = maze.start
    goal = maze.goal

    # Heap entries: (estimated total cost, actual cost, position).
    frontier = [(manhattan_distance(start, goal), 0, start)]
    came_from: Dict[Position, Position] = {}
    cost_so_far: Dict[Position, int] = {start: 0}
    expanded_nodes = 0
    expanded_order = []

    while frontier:
        _, current_cost, current = heapq.heappop(frontier)

        # Ignore outdated queue entries.
        if current_cost != cost_so_far.get(current):
            continue

        expanded_nodes += 1
        expanded_order.append(current)

        if current == goal:
            break

        for neighbor in maze.neighbors(current):
            new_cost = current_cost + 1

            if new_cost < cost_so_far.get(neighbor, float("inf")):
                cost_so_far[neighbor] = new_cost
                came_from[neighbor] = current

                priority = new_cost + manhattan_distance(neighbor, goal)
                heapq.heappush(
                    frontier,
                    (priority, new_cost, neighbor),
                )

    path = reconstruct_path(came_from, start, goal)
    runtime_ms = (time.perf_counter() - start_time) * 1000

    return {
        "algorithm": "A*",
        "path": path,
        "path_length": len(path) - 1 if path else None,
        "runtime_ms": runtime_ms,
        "expanded_nodes": expanded_nodes,
        "expanded_order": expanded_order,
        "success": bool(path),
    }
