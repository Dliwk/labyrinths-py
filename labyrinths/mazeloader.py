from labyrinths.labyrinth import LabyrinthData
from labyrinths.utils import load, dump
import gzip


def load_maze(path: str) -> LabyrinthData:
    with open(path, "rb") as file:
        return load(LabyrinthData, gzip.decompress(file.read()).decode())


def dump_maze(maze: LabyrinthData, path: str) -> None:
    with open(path, "wb") as file:
        file.write(gzip.compress(dump(maze).encode()))
