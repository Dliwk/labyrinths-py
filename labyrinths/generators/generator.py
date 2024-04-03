"""Module with base class for generators."""

from labyrinths.labyrinth import Cell, CellKind, LabyrinthData, WallKind


class LabyrinthGenerator:
    """Basic class for generating mazes."""

    def __init__(self, columns: int, rows: int) -> None:
        self.columns = columns
        self.rows = rows
        self.current: LabyrinthData = self.get_filled_maze(columns, rows)

    @classmethod
    def get_empty_maze(cls, columns: int, rows: int) -> LabyrinthData:
        """Gen dummy maze without any walls."""
        data = LabyrinthData(
            columns,
            rows,
            [
                [
                    Cell(
                        kind=CellKind.EMPTY,
                        left=WallKind.EMPTY,
                        right=WallKind.EMPTY,
                        up=WallKind.EMPTY,
                        down=WallKind.EMPTY,
                    )
                    for _ in range(rows)
                ]
                for _ in range(columns)
            ],
        )
        for x in range(columns):
            data.field[x][0].up = WallKind.WALL
            data.field[x][rows - 1].down = WallKind.WALL
        for y in range(rows):
            data.field[0][y].left = WallKind.WALL
            data.field[columns - 1][y].right = WallKind.WALL
        return data

    @classmethod
    def get_filled_maze(cls, columns: int, rows: int) -> LabyrinthData:
        """Get maze filled with walls."""
        return LabyrinthData(
            columns,
            rows,
            [
                [
                    Cell(
                        kind=CellKind.EMPTY,
                        left=WallKind.WALL,
                        right=WallKind.WALL,
                        up=WallKind.WALL,
                        down=WallKind.WALL,
                    )
                    for _ in range(rows)
                ]
                for _ in range(columns)
            ],
        )

    def generate(self) -> LabyrinthData:
        """Generate maze, virtual function."""
        raise NotImplementedError  # pragma: no cover

    def is_out_of_bounds(self, x: int, y: int) -> bool:
        """Check if (x, y) is out of bounds."""
        return not (0 <= x < self.columns and 0 <= y < self.rows)

    def set_wall_at(self, x: int, y: int, dx: int, dy: int, wallkind: WallKind) -> None:
        """Set wall between (x, y) and (x + dx, y + dy)."""
        self.current.field[x][y].set_wall_at(dx, dy, wallkind)
        self.current.field[x + dx][y + dy].set_wall_at(-dx, -dy, wallkind)
