"""Maze widget"""

import random

import pygame
from pygame import draw

from labyrinths.generators.kruskal import KruskalGenerator
from labyrinths.maze import MazeData, WallKind
from labyrinths.mazeloader import dump_maze, load_maze
from labyrinths.solver import MazeSolver, Solution
from labyrinths.ui import Widget
from labyrinths.ui.widgets.button import Button


class MazeWidget(Widget):
    """Maze widget"""

    def __init__(self, parent: Widget, width: int, height: int, x: int, y: int) -> None:
        super().__init__(parent, width, height, x, y)
        self.cellsize = 20
        self.wallwidth = 1
        self.solution_line_width = 4

        self.current_maze: MazeData | None = None
        self.maze_viewport = (0, 0)
        self.solution: Solution | None = None

        Button(self, 100, 30, 0, self.height - 30, onclick=self.new_maze, text="new maze")
        Button(self, 100, 30, self.width - 100, self.height - 30, onclick=self.show_solution, text="solution")
        Button(self, 30, 30, self.width - 30, 0, onclick=self.scale_up, text="+")
        Button(self, 30, 30, self.width - 60, 0, onclick=self.scale_down, text="-")
        Button(self, 60, 30, self.width - 60, self.height // 2, onclick=self.save_maze, text="save")
        Button(self, 60, 30, self.width - 60, self.height // 2 - 30, onclick=self.load_maze, text="load")

    def new_maze(self) -> None:
        self.set_maze(KruskalGenerator(random.randint(10, 60), random.randint(10, 50)).generate())

    def save_maze(self) -> None:
        assert self.current_maze
        dump_maze(self.current_maze, "maze.json.gz")

    def load_maze(self) -> None:
        self.set_maze(load_maze("maze.json.gz"))

    def show_solution(self) -> None:
        assert self.current_maze is not None
        self.solution = MazeSolver(self.current_maze).solve()

    def set_maze(self, maze: MazeData) -> None:
        self.current_maze = maze
        self.solution = None

    def _get_begin_of_cell(self, i: int, j: int) -> tuple[int, int]:
        return (
            i * self.cellsize - self.maze_viewport[0],
            j * self.cellsize - self.maze_viewport[1],
        )

    def _get_center_of_cell(self, i: int, j: int) -> tuple[int, int]:
        x, y = self._get_begin_of_cell(i, j)
        return x + self.cellsize // 2, y + self.cellsize // 2

    def draw_solution(self):
        """Draw the solution path of the current maze."""
        solution = self.solution
        for (i, j), (ni, nj) in zip(solution.path, solution.path[1:], strict=False):
            x, y = self._get_center_of_cell(i, j)
            nx, ny = self._get_center_of_cell(ni, nj)
            draw.line(self.surface, "red", (x, y), (nx, ny), self.solution_line_width)

    def scale_up(self):
        self.cellsize += 1

    def scale_down(self):
        self.cellsize -= 1

    def on_keydown(self, key: int) -> None:
        match key:
            case pygame.K_LEFT:
                self.maze_viewport = self.maze_viewport[0] - self.cellsize, self.maze_viewport[1]
            case pygame.K_RIGHT:
                self.maze_viewport = self.maze_viewport[0] + self.cellsize, self.maze_viewport[1]
            case pygame.K_UP:
                self.maze_viewport = self.maze_viewport[0], self.maze_viewport[1] - self.cellsize
            case pygame.K_DOWN:
                self.maze_viewport = self.maze_viewport[0], self.maze_viewport[1] + self.cellsize
            case pygame.K_o:
                self.scale_up()
            case pygame.K_p:
                self.scale_down()

    def draw_maze(self) -> None:
        """Draw the maze."""
        maze = self.current_maze
        assert maze is not None
        for i in range(maze.columns):
            for j in range(maze.rows):
                x, y = self._get_begin_of_cell(i, j)
                dx, dy = self.cellsize, self.cellsize
                draw.rect(
                    self.surface,
                    "white",
                    pygame.Rect(x, y, dx, dy),
                    0,
                )
                celldata = maze.field[i][j]
                if celldata.left is WallKind.WALL:
                    draw.rect(
                        self.surface,
                        "black",
                        pygame.Rect(x, y, self.wallwidth, dy),
                        0,
                    )
                if celldata.right is WallKind.WALL:
                    draw.rect(
                        self.surface,
                        "black",
                        pygame.Rect(x + dx - self.wallwidth, y, self.wallwidth, dy),
                        0,
                    )
                if celldata.up is WallKind.WALL:
                    draw.rect(
                        self.surface,
                        "black",
                        pygame.Rect(x, y, dx, self.wallwidth),
                        0,
                    )
                if celldata.down is WallKind.WALL:
                    draw.rect(
                        self.surface,
                        "black",
                        pygame.Rect(x, y + dy - self.wallwidth, dx, self.wallwidth),
                        0,
                    )

    def render(self) -> None:
        self.draw_maze()
        if self.solution:
            self.draw_solution()
