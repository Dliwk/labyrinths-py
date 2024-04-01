import random
from typing import override

from labyrinths.generators.generator import LabyrinthGenerator
from labyrinths.labyrinth import LabyrinthData, Cell, WallKind, CellKind


class DepthFirstSearchGenerator(LabyrinthGenerator):
    def __init__(self, columns: int, rows: int):
        super().__init__(columns, rows)
        self.visited: list[list[bool]] | None = None
        self.finished = False

    def _is_out_of_bounds(self, row: int, column: int) -> bool:
        return not (0 <= row < self.rows and 0 <= column < self.columns)

    def visit(self, column: int, row: int) -> None:
        assert self.current
        self.visited[column][row] = True

        order = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        random.shuffle(order)

        for dx, dy in order:
            x, y = row + dx, column + dy
            if self._is_out_of_bounds(x, y):
                self.finished = True
            elif not self.visited[x][y]:
                self.set_wall_at(row, column, dx, dy, WallKind.WALL)
                self.visit(x, y)
            if self.finished:
                return

    @override
    def generate(self) -> LabyrinthData:
        self.current = self.get_filled_maze(self.columns, self.rows)
        self.visited = [[False for _ in range(self.columns)] for _ in range(self.rows)]
        self.visit(self.rows // 2, self.columns // 2)
        return self.current
