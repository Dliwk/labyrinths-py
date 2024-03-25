import dataclasses
import json

from labyrinths.labyrinth import LabyrinthData, LabyrinthCell
from labyrinths.utils import dump, load


def main():
    lab = LabyrinthData(2, 2, [[LabyrinthCell.EMPTY, LabyrinthCell.WALL],
                               [LabyrinthCell.EMPTY, LabyrinthCell.EMPTY]])


if __name__ == '__main__':
    main()
