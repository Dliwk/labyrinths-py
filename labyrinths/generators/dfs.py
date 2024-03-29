import random
from typing import override

from labyrinths.generators.generator import LabyrinthGenerator
from labyrinths.labyrinth import LabyrinthData, LabyrinthCell


class DepthFirstSearchGenerator(LabyrinthGenerator):
    def __init__(self, rows: int, columns: int, wall_chance=0.7):
        self.rows = rows
        self.columns = columns
        self.wall_chance = wall_chance
        self.current: LabyrinthData | None = None
        self.visited: list[list[bool]] | None = None
        self.finished = False

    def _empty_neighbours_count(self, row: int, column: int) -> int:
        result = 0
        for dx, dy in (-1, 0), (1, 0), (0, -1), (0, 1):
            x, y = row + dx, column + dy
            if not self._is_out_of_bounds(x, y) and self.current.field[x][y] == LabyrinthCell.EMPTY:
                result += 1
        return result

    def _is_out_of_bounds(self, row: int, column: int) -> bool:
        return not (0 <= row < self.rows and 0 <= column < self.columns)

    def visit(self, row: int, column: int) -> None:
        assert self.current

        self.visited[row][column] = True
        self.current.field[row][column] = LabyrinthCell.EMPTY

        order = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        random.shuffle(order)

        for dx, dy in order:
            x, y = row + dx, column + dy
            if self._is_out_of_bounds(x, y):
                self.finished = True
            elif not self.visited[x][y] and self._empty_neighbours_count(x, y) == 1:
                self.visit(x, y)
            if self.finished:
                return

        self.current.field[row][column] = LabyrinthCell.WALL
        self.visited[row][column] = True

    @override
    def generate(self) -> LabyrinthData:
        self.current = LabyrinthData(self.rows, self.columns,
                                     [[LabyrinthCell.WALL if random.random() < self.wall_chance else LabyrinthCell.EMPTY
                                       for _ in range(self.columns)] for _ in range(self.rows)])
        self.visited = [[False for _ in range(self.columns)] for _ in range(self.rows)]
        self.visit(self.rows // 2, self.columns // 2)
        return self.current
