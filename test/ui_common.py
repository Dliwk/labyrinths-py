"""UI testing common functionality."""

import pygame
import pytest

from labyrinths.ui.mainwindow import Widget


@pytest.fixture
def pygame_headless():
    import os
    os.environ['SDL_VIDEODRIVER'] = "dummy"


class EmptyWidget(Widget):
    def render(self) -> None:
        pass
