"""Main entry point."""

import argparse
import sys

from labyrinths.generators.kruskal import KruskalGenerator
from labyrinths.maze import MazeData
from labyrinths.mazeloader import load_maze
from labyrinths.ui.widgets.button import Button
from labyrinths.ui.widgets.mazewindow import MazeWidget

# Для лучшей генерации
sys.setrecursionlimit(100_000)


def main() -> None:
    """Main function."""
    parser = argparse.ArgumentParser(prog="labyrinths", description="generate or solve mazes")
    parser.add_argument("-v", "--visual", help="run visualizer", action="store_true")
    # parser.add_argument('--loadfrom', help='load maze into visualizer window', type=argparse.FileType())
    # parser.add_argument("--loadfrom", help="load maze into visualizer window")
    # parser.add_argument("--size", help="select maze size", default="59,39")
    args = parser.parse_args()

    if args.visual:
        from labyrinths.ui.mainwindow import MainWindow

        mainwindow = MainWindow(800, 600)
        mazewidget = MazeWidget(mainwindow.root_widget, 800, 600, 0, 0)
        mazewidget.new_maze()
        mainwindow.run()


if __name__ == "__main__":
    main()
