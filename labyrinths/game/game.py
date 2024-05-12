"""Defines the Game class."""

import logging
from typing import Tuple

from labyrinths.generators.kruskal import KruskalGenerator
from labyrinths.maze import MazeData, WallKind
from labyrinths.session.types import Player

logger = logging.getLogger(__name__)


class Game:
    """Handles the game logic."""

    def __init__(self, w: int, h: int):
        gen = KruskalGenerator(w, h)
        self.maze: MazeData = gen.generate()
        self.players: dict[int, Player] = {}
        self.winner_id: int | None = None
        self.ended = False

    def handle_movement(self, client_id: int, direction: str) -> Tuple[int, int] | None:
        player = self.players[client_id]
        x, y = player.x, player.y
        match direction:
            case "up":
                dx, dy = 0, -1
            case "down":
                dx, dy = 0, 1
            case "left":
                dx, dy = -1, 0
            case "right":
                dx, dy = 1, 0
            case _:
                raise ValueError(f"Invalid direction: {direction}")
        if self.maze.field[x][y].get_wall_at(dx, dy) == WallKind.WALL:
            return

        player.x += dx
        player.y += dy

        if (player.x, player.y) == (self.maze.columns - 1, self.maze.rows - 1) and self.winner_id is None:
            self.winner_id = client_id

        return player.x, player.y
