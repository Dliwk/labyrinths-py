"""UI testing."""

import weakref

import pygame
import pytest

from labyrinths.ui.mainwindow import MainWindow, Widget


@pytest.fixture
def pygame_headless(mocker):
    def set_mode(size):
        return pygame.Surface(size)

    mocker.patch("pygame.init")
    mocker.patch("pygame.font.init")
    mocker.patch("pygame.display.set_mode", set_mode)


class EmptyWidget(Widget):
    def render(self) -> None:
        pass


def test_keydown(mocker, pygame_headless) -> None:
    mainwindow = MainWindow(800, 600)
    widget1 = EmptyWidget(mainwindow.root_widget, 30, 40, 10, 20)
    widget2 = EmptyWidget(mainwindow.root_widget, 30, 40, 10, 20)
    widget3 = EmptyWidget(widget2, 2, 3, 3, 3)

    spy1 = mocker.spy(widget1, "on_keydown")
    spy2 = mocker.spy(widget2, "on_keydown")
    spy3 = mocker.spy(widget3, "on_keydown")

    mainwindow.root_widget.on_keydown_propagate(pygame.K_a)

    spy1.assert_called_once_with(pygame.K_a)
    spy2.assert_called_once_with(pygame.K_a)
    spy3.assert_called_once_with(pygame.K_a)


def test_keyup(mocker, pygame_headless) -> None:
    mainwindow = MainWindow(800, 600)
    widget1 = EmptyWidget(mainwindow.root_widget, 30, 40, 10, 20)
    widget2 = EmptyWidget(mainwindow.root_widget, 30, 40, 10, 20)
    widget3 = EmptyWidget(widget2, 2, 3, 3, 3)

    spy1 = mocker.spy(widget1, "on_keyup")
    spy2 = mocker.spy(widget2, "on_keyup")
    spy3 = mocker.spy(widget3, "on_keyup")

    mainwindow.root_widget.on_keyup_propagate(pygame.K_a)

    spy1.assert_called_once_with(pygame.K_a)
    spy2.assert_called_once_with(pygame.K_a)
    spy3.assert_called_once_with(pygame.K_a)


def test_mouse_click(mocker, pygame_headless) -> None:
    mainwindow = MainWindow(800, 600)
    widget = EmptyWidget(mainwindow.root_widget, 30, 40, 10, 20)
    spy = mocker.spy(widget, "on_mouse_left_click")

    mainwindow.on_mouse_left_click(9, 19)
    assert spy.call_count == 0

    mainwindow.on_mouse_left_click(10, 20)
    assert spy.call_count == 1

    mainwindow.on_mouse_left_click(20, 30)
    assert spy.call_count == 2

    mainwindow.on_mouse_left_click(0, 80)
    assert spy.call_count == 2

    mainwindow.on_mouse_left_click(90, 0)
    assert spy.call_count == 2

    mainwindow.on_mouse_left_click(40, 50)
    assert spy.call_count == 2

    mainwindow.on_mouse_left_click(30, 60)
    assert spy.call_count == 2


def test_widget_closure(mocker, pygame_headless) -> None:
    mainwindow = MainWindow(800, 600)
    widget1 = EmptyWidget(mainwindow.root_widget, 30, 40, 10, 20)
    widget2 = EmptyWidget(widget1, 10, 20, 0, 0)

    widget2_has_dead = False

    def on_widget2_death() -> None:
        nonlocal widget2_has_dead
        widget2_has_dead = True

    weakref.finalize(widget2, on_widget2_death)
    widget1.close()
    del widget2
    del widget1
    # gc.collect()
    assert widget2_has_dead