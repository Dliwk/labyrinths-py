"""Common test functionality for generators."""

from labyrinths.labyrinth import LabyrinthData, WallKind


def check_maze_is_correctly_formed(maze: LabyrinthData) -> None:
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


def check_maze_has_solution(maze: LabyrinthData) -> None:
    """Check that the maze has a solution."""
    from labyrinths.solver import LabyrinthSolver

    # Raises an exception on failure
    LabyrinthSolver(maze).solve()
