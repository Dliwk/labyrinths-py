"""Test maze window UI."""

from ui_common import pygame_headless

from labyrinths.ui.mainwindow import MainWindow
from labyrinths.ui.widgets.mazewindow import MazeWidget


def test_maze_window(pygame_headless) -> None:
    """Test maze window runs successfully."""

    mainwindow = MainWindow(800, 600)
    mazewidget = MazeWidget(mainwindow.root_widget, 800, 600, 0, 0)

    mazewidget.new_maze()
    mazewidget.show_solution()
