
import unittest

from src.maze import Maze
from src.pathfinding import astar, dijkstra


class TestPathfinding(unittest.TestCase):

    def setUp(self):
        self.grid = [
            "S....",
            ".##..",
            "...#.",
            "##...",
            "....G",
        ]
        self.maze = Maze(self.grid)

    def test_both_algorithms_find_optimal_path(self):
        for algorithm in (astar, dijkstra):
            with self.subTest(algorithm=algorithm.__name__):
                result = algorithm(self.maze)

                self.assertTrue(result["success"])
                self.assertEqual(result["path_length"], 8)
                self.assertEqual(result["path"][0], self.maze.start)
                self.assertEqual(result["path"][-1], self.maze.goal)

    def test_path_uses_only_walkable_neighbors(self):
        for algorithm in (astar, dijkstra):
            result = algorithm(self.maze)
            path = result["path"]

            for current, following in zip(path, path[1:]):
                self.assertIn(following, self.maze.neighbors(current))

    def test_unreachable_goal(self):
        maze = Maze([
            "S#G",
            "###",
            "...",
        ])

        for algorithm in (astar, dijkstra):
            result = algorithm(maze)

            self.assertFalse(result["success"])
            self.assertIsNone(result["path_length"])
            self.assertEqual(result["path"], [])

    def test_adjacent_start_and_goal(self):
        maze = Maze(["SG"])

        for algorithm in (astar, dijkstra):
            result = algorithm(maze)

            self.assertTrue(result["success"])
            self.assertEqual(result["path_length"], 1)
            self.assertEqual(result["path"], [(0, 0), (0, 1)])

    def test_start_equals_goal_is_not_a_valid_maze(self):
        with self.assertRaises(ValueError):
            Maze(["S"])

    def test_invalid_maze_without_goal(self):
        with self.assertRaises(ValueError):
            Maze(["S.."])

    def test_invalid_maze_with_unequal_rows(self):
        with self.assertRaises(ValueError):
            Maze([
                "S..",
                "..G.",
            ])


if __name__ == "__main__":
    unittest.main(verbosity=2)
