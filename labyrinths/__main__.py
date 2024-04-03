"""Main entry point."""

import argparse
import sys

from labyrinths.maze import MazeData
from labyrinths.mazeloader import load_maze

# Для лучшей генерации
sys.setrecursionlimit(100_000)


def main() -> None:
    """Main function."""
    parser = argparse.ArgumentParser(prog="labyrinths", description="generate or solve mazes")
    parser.add_argument("-v", "--visual", help="run visualizer", action="store_true")
    # parser.add_argument('--loadfrom', help='load maze into visualizer window', type=argparse.FileType())
    parser.add_argument("--loadfrom", help="load maze into visualizer window")
    parser.add_argument("--size", help="select maze size", default="59,39")
    args = parser.parse_args()

    if args.visual:
        from labyrinths import visualizer

        if args.loadfrom is not None:
            maze: MazeData = load_maze(args.loadfrom)
            vis = visualizer.Visualizer(maze.columns, maze.rows)
            vis.run(maze)
        else:
            vis = visualizer.Visualizer(*map(int, args.size.split(",")))
            vis.run()


if __name__ == "__main__":
    main()
