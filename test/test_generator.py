import pytest
from generators_common import check_maze_has_solution

from labyrinths.generators.generator import LabyrinthGenerator
from labyrinths.labyrinth import LabyrinthData, WallKind
from labyrinths.solver import NoSolution


def check_maze_is_empty(maze: LabyrinthData) -> None:
    """Check that the maze is correctly formed"""

    def is_out_of_bounds(i: int, j: int) -> bool:
        return not (0 <= i < maze.columns and 0 <= j < maze.rows)

    for x in range(maze.columns):
        for y in range(maze.rows):
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                if is_out_of_bounds(x + dx, y + dy):
                    assert maze.field[x][y].get_wall_at(dx, dy) == WallKind.WALL
                else:
                    assert maze.field[x][y].get_wall_at(dx, dy) == WallKind.EMPTY


@pytest.mark.parametrize("size", [(1, 2), (2, 3), (4, 1), (1, 1), (4, 4)])
def test_maze_empty(size: tuple[int, int]) -> None:
    maze = LabyrinthGenerator.get_empty_maze(*size)
    check_maze_is_empty(maze)


def test_no_solution() -> None:
    maze = LabyrinthGenerator.get_filled_maze(2, 3)
    with pytest.raises(NoSolution):
        check_maze_has_solution(maze)
