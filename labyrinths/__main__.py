from labyrinths.labyrinth import LabyrinthData
from labyrinths.mazeloader import load_maze
import sys
import argparse

# Для лучшей генерации
sys.setrecursionlimit(100_000)


def main():
    parser = argparse.ArgumentParser(prog='labyrinths', description='generate or solve mazes')
    parser.add_argument('-v', '--visual', help='run visualizer', action='store_true')
    # parser.add_argument('--loadfrom', help='load maze into visualizer window', type=argparse.FileType())
    parser.add_argument('--loadfrom', help='load maze into visualizer window')
    args = parser.parse_args()

    if args.visual:
        import visualizer

        if args.loadfrom is not None:
            maze: LabyrinthData = load_maze(args.loadfrom)
            vis = visualizer.Visualizer(maze.columns, maze.rows)
            vis.run(maze)
        else:
            vis = visualizer.Visualizer(40, 30)
            vis.run()


if __name__ == "__main__":
    main()
