
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
