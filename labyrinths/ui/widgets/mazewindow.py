"""Maze widget"""

import random

import pygame
from pygame import draw

from labyrinths.generators.dfs import DepthFirstSearchGenerator
from labyrinths.generators.kruskal import KruskalGenerator
from labyrinths.maze import MazeData, WallKind
from labyrinths.mazeloader import dump_maze, load_maze
from labyrinths.solver import MazeSolver, Solution
from labyrinths.ui import Widget
from labyrinths.ui.widgets.button import Button
from labyrinths.ui.widgets.label import TextLabel


class MazeWidget(Widget):
    """Maze widget"""

    def __init__(self, parent: Widget, width: int, height: int, x: int, y: int) -> None:
        super().__init__(parent, width, height, x, y)
        self.cellsize = 20
        self.wallwidth = 1
        self.solution_line_width = 4

        self.current_maze: MazeData | None = None
        self.maze_viewport = (-self.cellsize * 3, -self.cellsize * 3)
        self.solution: Solution | None = None

        self.generators = [
            (KruskalGenerator, "Kruskal MST"),
            (DepthFirstSearchGenerator, "DFS"),
        ]
        self.gen_id = 0

        self.help_widget = TextLabel(
            self,
            300,
            300,
            30,
            30,
            # fmt: off
            text=("Use arrows keys to move.\n"
                  "WASD to look around.\n"
                  "By default, mazes\n"
                  "are saved into\n"
                  "maze.json.gz"),
            # fmt: on
        )
        self.help_widget.hide()

        Button(self, 100, 30, 0, self.height - 30, onclick=self.new_maze, text="new maze")
        self.next_gen_button = Button(self, 120, 30, 0, self.height - 60, onclick=self.next_gen, text="")
        Button(self, 100, 30, self.width - 100, self.height - 30, onclick=self.toggle_solution, text="solution")
        Button(self, 30, 30, self.width - 30, 0, onclick=self.scale_up, text="+")
        Button(self, 30, 30, self.width - 60, 0, onclick=self.scale_down, text="-")
        Button(self, 60, 30, self.width - 60, self.height // 2, onclick=self.save_maze, text="save")
        Button(self, 60, 30, self.width - 60, self.height // 2 - 30, onclick=self.load_maze, text="load")
        Button(self, 30, 30, 0, 0, onclick=self.toggle_help, text="?")

        self.next_gen()

        self.player_coordinates = (0, 0)

    def next_gen(self):
        self.gen_id += 1
        if self.gen_id == len(self.generators):
            self.gen_id = 0
        self.next_gen_button.text = self.generators[self.gen_id][1]

    def toggle_help(self):
        self.help_widget.toggle()

    def new_maze(self) -> None:
        gen_class = self.generators[self.gen_id][0]
        self.set_maze(gen_class(random.randint(10, 60), random.randint(10, 50)).generate())

    def save_maze(self) -> None:
        assert self.current_maze
        dump_maze(self.current_maze, "maze.json.gz")

    def load_maze(self) -> None:
        self.set_maze(load_maze("maze.json.gz"))

    def toggle_solution(self) -> None:
        if self.solution is not None:
            self.solution = None
        else:
            self.show_solution()

    def show_solution(self) -> None:
        assert self.current_maze
        self.solution = MazeSolver(self.current_maze).solve()

    def set_maze(self, maze: MazeData) -> None:
        self.player_coordinates = (0, 0)
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

    def try_move_player(self, dx: int, dy: int) -> None:
        """Try to move player at given direction"""
        x, y = self.player_coordinates
        assert self.current_maze
        if self.current_maze.field[x][y].get_wall_at(dx, dy) == WallKind.EMPTY:
            self.player_coordinates = (x + dx, y + dy)
            self.check_end_game()

    def check_end_game(self):
        if self.player_coordinates == (self.current_maze.columns - 1, self.current_maze.rows - 1):
            self.show_solution()

    def on_keydown(self, key: int) -> None:
        match key:
            case pygame.K_a:
                self.maze_viewport = self.maze_viewport[0] - self.cellsize, self.maze_viewport[1]
            case pygame.K_d:
                self.maze_viewport = self.maze_viewport[0] + self.cellsize, self.maze_viewport[1]
            case pygame.K_w:
                self.maze_viewport = self.maze_viewport[0], self.maze_viewport[1] - self.cellsize
            case pygame.K_s:
                self.maze_viewport = self.maze_viewport[0], self.maze_viewport[1] + self.cellsize
            case pygame.K_o:
                self.scale_up()
            case pygame.K_p:
                self.scale_down()
            case pygame.K_UP:
                self.try_move_player(0, -1)
            case pygame.K_LEFT:
                self.try_move_player(-1, 0)
            case pygame.K_DOWN:
                self.try_move_player(0, 1)
            case pygame.K_RIGHT:
                self.try_move_player(1, 0)

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
        draw.circle(
            self.surface,
            "green",
            self._get_center_of_cell(*self.player_coordinates),
            (self.cellsize - self.wallwidth) // 2,
        )

    def render(self) -> None:
        self.draw_maze()
        if self.solution:
            self.draw_solution()
