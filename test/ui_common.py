"""UI testing common functionality."""

import pygame
import pytest

from labyrinths.ui.mainwindow import Widget


@pytest.fixture
def pygame_headless(mocker):
    def set_mode(size):
        return pygame.Surface(size)

    mocker.patch("pygame.init")
    mocker.patch("pygame.font.init")
    mocker.patch("pygame.font.Font")
    mocker.patch("pygame.display.set_mode", set_mode)


class EmptyWidget(Widget):
    def render(self) -> None:
        pass
