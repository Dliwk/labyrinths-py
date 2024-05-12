"""Main entry point."""

import argparse
import sys

# Для лучшей генерации
sys.setrecursionlimit(100_000)


def main() -> None:
    """Main function."""
    parser = argparse.ArgumentParser(prog="labyrinths", description="generate or solve mazes")
    parser.add_argument("-c", "--cli", help="do not run GUI", action="store_true")
    parser.add_argument("--loadfrom", help="load maze into GUI window", metavar="FILE")

    parser.add_argument("--generate", help="generate and save maze into file", metavar="FILE")
    parser.add_argument("--size", help="select maze size for generation", default="59,39")
    parser.add_argument("--algo", help="select generation algorithm", default="mst", nargs="?", choices=["mst", "dfs"])
    args = parser.parse_args()

    if not args.cli:
        from labyrinths.starter import main

        main()

    elif args.generate:
        from labyrinths.generators.dfs import DepthFirstSearchGenerator
        from labyrinths.generators.kruskal import KruskalGenerator
        from labyrinths.mazeloader import dump_maze

        dest = args.generate
        gen_class = KruskalGenerator if args.algo == "mst" else DepthFirstSearchGenerator
        size = map(int, args.size.split(","))
        maze = gen_class(*size).generate()
        dump_maze(maze, dest)
        print(f'OK! Maze saved to "{dest}"')
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
