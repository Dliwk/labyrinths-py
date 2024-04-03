"""Simple module to visualize maze using pygame"""

import random
import sys

import pygame
from pygame import draw

from labyrinths.generators.dfs import DepthFirstSearchGenerator
from labyrinths.generators.kruskal import KruskalGenerator
from labyrinths.labyrinth import LabyrinthData, WallKind
from labyrinths.mazeloader import dump_maze
from labyrinths.solver import LabyrinthSolver, Solution

pygame.init()
pygame.font.init()


class Visualizer:
    """Main class to visualize mazes."""

    def __init__(self, columns: int, rows: int) -> None:
        self.columns = columns
        self.rows = rows
        self.cellwidth = 50 if columns < 10 else 20 if columns < 60 else 10 if columns < 120 else 5
        self.cellheight = 50 if rows < 10 else 20 if rows < 40 else 10 if rows < 80 else 5
        self.cellwidth = self.cellheight = min(self.cellwidth, self.cellheight)
        self.wallwidth = 1

        self.globalwidth = self.columns * self.cellwidth + self.cellwidth * 2
        self.globalheight = self.rows * self.cellheight + self.cellheight * 2
        self.globalscreen = pygame.display.set_mode((self.globalwidth, self.globalheight))
        self.globalscreen.fill("white")
        self.screen = self.globalscreen.subsurface(
            pygame.Rect(
                self.cellwidth,
                self.cellheight,
                self.columns * self.cellwidth,
                self.rows * self.cellheight,
            )
        )

        self.font = pygame.font.Font(None, self.cellheight)

        self.current_maze: LabyrinthData | None = None
        self.current_solution: Solution | None = None

    def draw_maze(self, maze: LabyrinthData) -> None:
        """Draw the given maze on the screen."""
        self.current_maze = maze
        self.current_solution = LabyrinthSolver(maze).solve()

        for i in range(maze.columns):
            for j in range(maze.rows):
                x, y = self._get_begin_of_cell(i, j)
                dx, dy = self.cellwidth, self.cellheight
                draw.rect(
                    self.screen,
                    "white",
                    pygame.Rect(x, y, dx, dy),
                    0,
                )
                celldata = maze.field[i][j]
                if celldata.left is WallKind.WALL:
                    draw.rect(
                        self.screen,
                        "black",
                        pygame.Rect(x, y, self.wallwidth, dy),
                        0,
                    )
                if celldata.right is WallKind.WALL:
                    draw.rect(
                        self.screen,
                        "black",
                        pygame.Rect(x + dx - self.wallwidth, y, self.wallwidth, dy),
                        0,
                    )
                if celldata.up is WallKind.WALL:
                    draw.rect(
                        self.screen,
                        "black",
                        pygame.Rect(x, y, dx, self.wallwidth),
                        0,
                    )
                if celldata.down is WallKind.WALL:
                    draw.rect(
                        self.screen,
                        "black",
                        pygame.Rect(x, y + dy - self.wallwidth, dx, self.wallwidth),
                        0,
                    )

        self.draw_solution()

    def _get_begin_of_cell(self, i: int, j: int) -> tuple[int, int]:
        return (
            i * self.cellwidth,
            j * self.cellheight,
        )

    def _get_center_of_cell(self, i: int, j: int) -> tuple[int, int]:
        x, y = self._get_begin_of_cell(i, j)
        return x + self.cellwidth // 2, y + self.cellheight // 2

    def draw_solution(self):
        """Draw the solution path of the current maze on the screen."""
        for (i, j), (ni, nj) in zip(self.current_solution.path, self.current_solution.path[1:], strict=False):
            x, y = self._get_center_of_cell(i, j)
            nx, ny = self._get_center_of_cell(ni, nj)

            draw.line(self.screen, "red", (x, y), (nx, ny), 4)

    def new_maze(self) -> None:
        """Draw the new maze on the screen."""
        generator_class, generator_args, algoname = random.choice(
            (
                (
                    DepthFirstSearchGenerator,
                    (self.columns, self.rows),
                    "Depth First Search",
                ),
                (KruskalGenerator, (self.columns, self.rows), "Kruskal"),
            )
        )
        generator = generator_class(*generator_args)

        maze = generator.generate()
        self.draw_maze(maze)

        self.set_algoname(algoname)

    def set_algoname(self, algoname: str) -> None:
        """Set the algorithm name on the bottom corner of the screen."""
        draw.rect(
            self.globalscreen,
            "white",
            pygame.Rect(
                0,
                self.globalheight - self.cellheight,
                self.globalwidth,
                self.cellheight,
            ),
        )
        text = self.font.render(algoname, True, "black")
        self.globalscreen.blit(text, (0, self.globalheight - self.cellheight))

    def run(self, maze: LabyrinthData | None = None):
        """Run the visualizer event loop."""
        pygame.display.set_caption("Labyrinths")

        text = self.font.render("Mouse click to generate a maze! Press space to save to file", True, "black")
        self.globalscreen.blit(text, (0, 0))

        if maze is not None:
            self.draw_maze(maze)
            self.set_algoname("Loaded from file")
        else:
            self.new_maze()

        while True:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    case pygame.MOUSEBUTTONDOWN:
                        self.new_maze()
                    case pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            assert self.current_maze
                            dump_maze(self.current_maze, "maze.json.gz")

                pygame.display.flip()
