"""Test UI buttons."""

from ui_common import EmptyWidget, pygame_headless

from labyrinths.ui.mainwindow import MainWindow
from labyrinths.ui.widgets.button import Button


class Callback:
    def __init__(self):
        self.call_count = 0

    def __call__(self, *args, **kwargs):
        self.call_count += 1


def test_button_click(pygame_headless) -> None:
    callback = Callback()
    mainwindow = MainWindow(800, 600)
    Button(mainwindow.root_widget, 40, 40, 80, 80, callback)

    mainwindow.on_mouse_left_click(80, 80)
    assert callback.call_count == 1

    mainwindow.on_mouse_left_click(120, 100)
    assert callback.call_count == 1

    mainwindow.on_mouse_left_click(100, 120)
    assert callback.call_count == 1

    mainwindow.on_mouse_left_click(100, 100)
    assert callback.call_count == 2

    mainwindow.on_mouse_left_click(100, 20)
    assert callback.call_count == 2

    mainwindow.on_mouse_left_click(20, 100)
    assert callback.call_count == 2


def test_overlapping_buttons(pygame_headless) -> None:
    callback1 = Callback()
    callback2 = Callback()
    callback3 = Callback()

    def call_counts():
        return callback1.call_count, callback2.call_count, callback3.call_count

    # 40..70
    mainwindow = MainWindow(800, 600)
    widget = EmptyWidget(mainwindow.root_widget, 100, 100, 0, 0)
    Button(widget, 30, 30, 40, 40, callback1)

    # 50..100
    nested_widget = EmptyWidget(widget, 50, 50, 50, 50)
    Button(nested_widget, 50, 50, 0, 0, callback2)

    # this button has higher z-index
    # 55..65
    Button(mainwindow.root_widget, 10, 10, 55, 55, callback3)

    mainwindow.on_mouse_left_click(60, 60)
    assert call_counts() == (0, 0, 1)

    mainwindow.on_mouse_left_click(50, 50)
    assert call_counts() == (0, 1, 1)

    mainwindow.on_mouse_left_click(67, 67)
    assert call_counts() == (0, 2, 1)

    mainwindow.on_mouse_left_click(45, 45)
    assert call_counts() == (1, 2, 1)
