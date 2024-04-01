import dataclasses
import json

import labyrinths.generators.dfs
from labyrinths.labyrinth import LabyrinthData, Cell
from labyrinths.utils import dump, load


def main():
    generator = labyrinths.generators.dfs.DepthFirstSearchGenerator(10, 10)
    # maze = generator.current
    maze = generator.generate()
    # print(maze)
    # print(dump(maze))
    zxc = load(LabyrinthData, dump(maze))
    print(json.dumps(json.loads(dump(maze)), indent=2))
    print(zxc)
    # zxc.


if __name__ == "__main__":
    main()
