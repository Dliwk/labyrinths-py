from dataclasses import dataclass
import enum


class LabyrinthCell(enum.Enum):
    EMPTY = 0
    WALL = 1


@dataclass
class LabyrinthData:
    """Хранит вид лабиринта - стены, проходы, размер"""
    rows: int
    columns: int

    field: list[list[LabyrinthCell]]

    def __str__(self) -> str:
        res = 'LabyrinthData(\n'
        for row in self.field:
            for cell in row:
                res += '#' if cell is LabyrinthCell.WALL else '.'
            res += '\n'
        return res + ')'
