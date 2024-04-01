from labyrinths.labyrinth import LabyrinthData, WallKind, CellKind, Cell


class LabyrinthGenerator:
    def __init__(self, columns: int, rows: int) -> None:
        self.columns = columns
        self.rows = rows
        self.current: LabyrinthData = self.get_empty_maze(columns, rows)

    def get_empty_maze(self, columns: int, rows: int) -> LabyrinthData:
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
        for x in range(self.columns):
            data.field[x][0].up = WallKind.WALL
            data.field[x][rows - 1].down = WallKind.WALL
        for y in range(self.rows):
            data.field[0][y].left = WallKind.WALL
            data.field[columns - 1][y].right = WallKind.WALL
        return data

    def get_filled_maze(self, columns: int, rows: int) -> LabyrinthData:
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
        raise NotImplementedError

    def is_out_of_bounds(self, x: int, y: int) -> bool:
        return not (0 <= x < self.columns and 0 <= y < self.rows)

    def set_wall_at(self, x: int, y: int, dx: int, dy: int, wallkind: WallKind) -> None:
        match (dx, dy):
            case (-1, 0):
                self.current.field[x][y].left = wallkind
                self.current.field[x - 1][y].right = wallkind
            case (1, 0):
                self.current.field[x][y].right = wallkind
                self.current.field[x + 1][y].left = wallkind
            case (0, -1):
                self.current.field[x][y].down = wallkind
                self.current.field[x][y - 1].up = wallkind
            case (0, 1):
                self.current.field[x][y].up = wallkind
                self.current.field[x][y + 1].down = wallkind
