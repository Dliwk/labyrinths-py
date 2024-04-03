"""Common test functionality for generators."""

from labyrinths.maze import MazeData, WallKind


def check_maze_is_correctly_formed(maze: MazeData) -> None:
    """Check that the maze is correctly formed"""

    def is_out_of_bounds(i: int, j: int) -> bool:
        return not (0 <= i < maze.columns and 0 <= j < maze.rows)

    for x in range(maze.columns):
        for y in range(maze.rows):
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                if is_out_of_bounds(x + dx, y + dy):
                    assert maze.field[x][y].get_wall_at(dx, dy) == WallKind.WALL
                else:
                    assert maze.field[x][y].get_wall_at(dx, dy) == maze.field[x + dx][y + dy].get_wall_at(-dx, -dy)


def check_maze_has_solution(maze: MazeData) -> None:
    """Check that the maze has a solution."""
    from labyrinths.solver import MazeSolver

    # Raises an exception on failure
    MazeSolver(maze).solve()
