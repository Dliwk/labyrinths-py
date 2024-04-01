import dataclasses
import json

import labyrinths.generators.dfs
from labyrinths.labyrinth import LabyrinthData, Cell
from labyrinths.utils import dump, load
import sys


def main():
    sys.setrecursionlimit(100_000)
    import visualizer

    vis = visualizer.Visualizer(40, 30)
    vis.run()


if __name__ == "__main__":
    main()
