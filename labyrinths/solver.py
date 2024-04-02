"""Solver for labyrinths."""

from collections import deque
from dataclasses import dataclass

from labyrinths.labyrinth import LabyrinthData, WallKind


@dataclass
class Solution:
    path: list[(int, int)]


class NoSolution(Exception):
    pass


class LabyrinthSolver:
    """Solver for labyrinths."""

    def __init__(
            self,
            maze: LabyrinthData,
            begin: (int, int) = (0, 0),
            end: tuple[int, int] | None = None,
    ) -> None:
        self.begin = begin
        self.end = end or (maze.columns - 1, maze.rows - 1)
        self.size = maze.columns, maze.rows
        self.maze = maze

        self.visited = [[False for _ in range(maze.rows)] for _ in range(maze.columns)]
        self.previous: dict[(int, int), (int, int)] = {}
        self.finished = False

    def solve(self) -> Solution:
        """Solve the labyrinth."""

        queue = deque([self.begin])
        self.visited[self.begin[0]][self.begin[1]] = True
        while queue:
            x, y = queue.popleft()
            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nx, ny = x + dx, y + dy
                if (
                        self.maze.field[x][y].get_wall_at(dx, dy) == WallKind.EMPTY
                        and 0 <= nx < self.size[0]
                        and 0 <= ny < self.size[1]
                        and not self.visited[nx][ny]
                ):
                    self.visited[nx][ny] = True
                    self.previous[(nx, ny)] = (x, y)
                    queue.append((nx, ny))

        path = []

        current = self.end
        while current != self.begin:
            path.append(current)
            try:
                current = self.previous[current]
            except KeyError:
                raise NoSolution
        path.append(self.begin)
        path.reverse()

        return Solution(path)
