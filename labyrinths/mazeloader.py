"""Utility functions for loading and storing mazes in files."""

import gzip
from os import PathLike

from labyrinths.labyrinth import LabyrinthData
from labyrinths.utils import dump, load


def load_maze(path: PathLike | str) -> LabyrinthData:
    """Load a maze from given path"""
    with open(path, "rb") as file:
        return load(LabyrinthData, gzip.decompress(file.read()).decode())


def dump_maze(maze: LabyrinthData, path: PathLike | str) -> None:
    """Dump a maze into given path. Usually extension is .json.gz"""
    with open(path, "wb") as file:
        file.write(gzip.compress(dump(maze).encode()))
