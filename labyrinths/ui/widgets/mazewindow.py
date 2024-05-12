"""Maze widget"""

from __future__ import annotations

import random
from typing import TYPE_CHECKING, Callable, Tuple

import pygame
from pygame import draw

from labyrinths.maze import MazeData, WallKind
from labyrinths.solver import MazeSolver, Solution
from labyrinths.ui import Widget
from labyrinths.ui.widgets.button import Button
from labyrinths.ui.widgets.label import TextLabel

if TYPE_CHECKING:
    from labyrinths.session.types import Player


class MazeWidget(Widget):
    """Maze widget"""

    def __init__(self, parent: Widget, width: int, height: int, x: int, y: int) -> None:
        super().__init__(parent, width, height, x, y)
        self.scale = 1.0
        self.current_maze: MazeData | None = None
        self.maze_real_viewport = (-self.cellsize * 3.0, -self.cellsize * 3.0)

        self.player_name_font = pygame.font.Font(None, 18)
        self.announcement_font = pygame.font.Font(None, 64)

        self.on_move_right: Callable[[], None] = lambda: None
        self.on_move_left: Callable[[], None] = lambda: None
        self.on_move_up: Callable[[], None] = lambda: None
        self.on_move_down: Callable[[], None] = lambda: None

        self.mouse_pressed = False

        self.help_widget = TextLabel(
            self,
            400,
            200,
            30,
            30,
            # fmt: off
            text=("Use arrow keys to move.\n"
                  "WASD or left-click&drag to look around.\n"
                  "Mouse scrolling is supported.\n"
                  "By default, mazes\n"
                  "are saved to\n"
                  "maze.json.gz"),
            # fmt: on
        )
        self.help_widget.hide()
        self.help_button = Button(self, 30, 30, 0, 0, onclick=self.toggle_help, text="?")

        Button(self, 30, 30, self.width - 30, 0, onclick=self.scale_up, text="+")
        Button(self, 30, 30, self.width - 60, 0, onclick=self.scale_down, text="-")

        self.players: dict[int, Player] | None = None

        self.solution: Solution | None = None
        self.winner_name: str | None = None
        self.winner_color: Tuple[int, int, int] | None = None

    @property
    def cellsize(self) -> int:
        return int(20 * self.scale)

    @property
    def wallwidth(self) -> int:
        return max(1, int(1 * self.scale))

    @property
    def solution_line_width(self) -> int:
        return max(1, int(4 * self.scale))

    # def next_gen(self):
    #     """Select next generator."""
    #     self.gen_id += 1
    #     if self.gen_id == len(self.generators):
    #         self.gen_id = 0
    #     self.next_gen_button.text = self.generators[self.gen_id][1]

    def toggle_help(self):
        """Show/hide help message."""
        if self.help_widget.hidden:
            self.help_widget.show()
            self.help_button.text = "x"
        else:
            self.help_widget.hide()
            self.help_button.text = "?"

    # def new_maze(self) -> None:
    #     """Generate new maze."""
    #     gen_class = self.generators[self.gen_id][0]
    #     self.set_maze(gen_class(random.randint(10, 60), random.randint(10, 50)).generate())

    # def save_maze(self) -> None:
    #     """Save the maze into file."""
    #     from labyrinths.mazeloader import dump_maze
    #
    #     assert self.current_maze
    #     dump_maze(self.current_maze, "maze.json.gz")

    # def load_maze(self) -> None:
    #     self.set_maze(load_maze("maze.json.gz"))

    # def toggle_solution(self) -> None:
    #     """Show/hide solution."""
    #     if self.solution is not None:
    #         self.solution = None
    #     else:
    #         self.show_solution()

    def show_solution(self) -> None:
        """Show solution."""
        assert self.current_maze
        self.solution = MazeSolver(self.current_maze).solve()

    def set_maze(self, maze: MazeData) -> None:
        self.current_maze = maze

    def set_players(self, player_list: dict[int, Player]) -> None:
        self.players = player_list

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
        """Scale up the maze."""
        self.scale_maze(3)

    def scale_down(self):
        """Scale down the maze."""
        self.scale_maze(-3)

    def on_keydown(self, key: int, event: pygame.Event) -> None:
        match key:
            case pygame.K_UP:
                self.on_move_up()
            case pygame.K_LEFT:
                self.on_move_left()
            case pygame.K_DOWN:
                self.on_move_down()
            case pygame.K_RIGHT:
                self.on_move_right()

    def on_mouse_left_button_down(self) -> None:
        self.mouse_pressed = True

    def on_mouse_left_button_up(self) -> None:
        self.mouse_pressed = False

    def on_mouse_motion(self, dx: int, dy: int) -> None:
        if self.mouse_pressed:
            x, y = self.maze_real_viewport
            self.maze_real_viewport = x - dx, y - dy

    @property
    def maze_viewport(self) -> tuple[int, int]:
        return int(self.maze_real_viewport[0]), int(self.maze_real_viewport[1])

    def scale_maze(self, amplitude: float) -> None:
        multiplier = pow(1.03, amplitude)
        self.scale *= multiplier
        x, y = self.maze_real_viewport
        # xoffset, yoffset = self.width / (2 * self.cellsize), self.height / (2 * self.cellsize)
        self.maze_real_viewport = (x * multiplier + self.width / 2 * (multiplier - 1)), (
                y * multiplier + self.height / 2 * (multiplier - 1)
        )

    def on_mouse_wheel(self, wheel: int) -> None:
        self.scale_maze(wheel)

    def draw_maze(self) -> None:
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

    def draw_players(self) -> None:
        for player in self.players.values():
            x, y = self._get_center_of_cell(player.x, player.y)
            draw.circle(
                self.surface,
                player.client.color,
                (x, y),
                (self.cellsize - self.wallwidth) // 2,
            )
            rendered_text = self.player_name_font.render(player.client.name, True, player.client.color)
            xsize, ysize = rendered_text.get_size()
            self.surface.blit(rendered_text, (x - xsize // 2, y - self.cellsize - ysize // 2))

    def draw_winner(self) -> None:
        rendered_text = self.announcement_font.render(f"{self.winner_name} wins", True, self.winner_color)
        xsize, ysize = rendered_text.get_size()
        self.surface.blit(rendered_text, (self.width // 2 - xsize // 2, 100))

    def render(self) -> None:
        if self.current_maze is not None:
            self.draw_maze()
            if self.solution:
                self.draw_solution()
            self.draw_players()
            if self.winner_name is not None:
                self.draw_winner()
