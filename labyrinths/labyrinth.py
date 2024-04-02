"""Module containing classes related to labyrinth data."""

from dataclasses import dataclass
from utils import transposed
import enum


class CellKind(enum.Enum):
    """Kind of cell. Currently, there is only one."""
    EMPTY = 0


class WallKind(enum.Enum):
    """Kind of wall."""
    EMPTY = 0
    WALL = 1


@dataclass
class Cell:
    """Cell data."""
    kind: CellKind
    left: WallKind
    right: WallKind
    up: WallKind
    down: WallKind

    def set_wall_at(self, dx: int, dy: int, wallkind: WallKind) -> None:
        """Set wall facing (dx, dy) direction."""
        match (dx, dy):
            case (-1, 0):
                self.left = wallkind
            case (1, 0):
                self.right = wallkind
            case (0, -1):
                self.down = wallkind
            case (0, 1):
                self.up = wallkind
            case _:
                raise Exception

    def get_wall_at(self, dx: int, dy: int) -> WallKind:
        """Get wall facing (dx, dy) direction."""
        match (dx, dy):
            case (-1, 0):
                return self.left
            case (1, 0):
                return self.right
            case (0, -1):
                return self.down
            case (0, 1):
                return self.up
            case _:
                raise Exception


@dataclass
class LabyrinthData:
    """Stores labyrinth data."""

    columns: int
    rows: int

    field: list[list[Cell]]
