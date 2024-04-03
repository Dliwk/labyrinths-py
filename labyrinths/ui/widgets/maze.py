"""Maze widget"""

from labyrinths.maze import MazeData
from labyrinths.ui.mainwindow import Widget


class MazeWidget(Widget):
    """Maze widget"""

    def __init__(self, parent: Widget, width: int, height: int, x: int, y: int) -> None:
        super().__init__(parent, width, height, x, y)
        self.cellsize = 5
        self.wallwidth = 1
        self.current_maze: MazeData | None = None
        self.maze_viewport = (0, 0)

    def set_maze(self, maze: MazeData) -> None:
        self.current_maze = maze

    def render(self) -> None:
        pass
