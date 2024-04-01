from dataclasses import dataclass
from utils import transposed
import enum


class CellKind(enum.Enum):
    EMPTY = 0


class WallKind(enum.Enum):
    EMPTY = 0
    WALL = 1


@dataclass
class Cell:
    kind: CellKind
    left: WallKind
    right: WallKind
    up: WallKind
    down: WallKind

    # TODO:
    # def __str__(self):
    #     match (self.left.value, self.right.value, self.up.value, self.down.value):
    #         case (0, 0, 0, 0):
    #             return ' '
    #         case (0, 0, 0, 1):
    #             return '🬭'  # '🭻'
    #         case (0, 0, 1, 0):
    #             return '🬂'  # '🭶'
    #         case (0, 1, 0, 0):
    #             return '🭋'  # '🭵'
    #         case (1, 0, 0, 0):
    #             return '🭀'  # '🭰'
    #         case (1, 0, 1, 0):
    #             return ' ' # '🭽'
    #         case (0, 1, 0, 1):
    #             return  # '🭿'
    #         case (1, 0, 0, 1):
    #             return  # '🭼'
    #         case (0, 1, 1, 0):
    #             return  # '🭾'
    #     return '🯄'


@dataclass
class LabyrinthData:
    """Хранит вид лабиринта - стены, проходы, размер"""

    columns: int
    rows: int

    field: list[list[Cell]]

    # TODO
    # def __str__(self) -> str:
    #     result = [[' ' for _ in range(self.columns)] for _ in range(self.rows)]
    #
    #     for x in range(self.columns):
    #         for y in range(self.rows):
    #             result[y][x] = str(self.field[x][y])
    #
    #     s = '\n'.join(''.join(line) for line in result)
    #     return f'LabyrinthData(\n{s}\n)'
