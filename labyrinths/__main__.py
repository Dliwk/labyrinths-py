import dataclasses
import json

import labyrinths.generators.dfs
from labyrinths.labyrinth import LabyrinthData, LabyrinthCell
from labyrinths.utils import dump, load


def main():
    generator = labyrinths.generators.dfs.DepthFirstSearchGenerator(30, 80)
    maze = generator.generate()
    # print(maze)
    # print(dump(maze))
    zxc = load(LabyrinthData, dump(maze))
    print(zxc)
    # zxc.


if __name__ == '__main__':
    main()
