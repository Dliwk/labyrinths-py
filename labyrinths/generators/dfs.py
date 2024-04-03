"""Generate mazes using depth first search algorithm."""

import random
from typing import override

from labyrinths.generators.generator import LabyrinthGenerator
from labyrinths.labyrinth import LabyrinthData, WallKind


class DepthFirstSearchGenerator(LabyrinthGenerator):
    """Generate mazes using depth first search."""

    def __init__(self, columns: int, rows: int):
        super().__init__(columns, rows)
        self.visited: list[list[bool]] | None = None

    def visit(self, x: int, y: int) -> None:
        """Visit cell."""
        assert self.current
        assert self.visited is not None
        self.visited[x][y] = True

        order = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        random.shuffle(order)

        for dx, dy in order:
            if not self.is_out_of_bounds(x + dx, y + dy) and not self.visited[x + dx][y + dy]:
                self.set_wall_at(x, y, dx, dy, WallKind.EMPTY)
                self.visit(x + dx, y + dy)

    @override
    def generate(self) -> LabyrinthData:
        """Generate maze."""
        self.visited = [[False for _ in range(self.rows)] for _ in range(self.columns)]
        self.visit(self.columns // 2, self.rows // 2)
        return self.current
