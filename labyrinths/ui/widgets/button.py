"""Simple UI button widget."""

from typing import Callable

import pygame
from pygame import draw

from labyrinths.ui import Widget


class Button(Widget):
    """A simple button widget."""

    def __init__(
        self,
        parent: Widget,
        width: int,
        height: int,
        x: int,
        y: int,
        onclick: Callable[[], None],
        text: str = "button",
        color: tuple[int, int, int] = (200, 200, 200),
        text_color: tuple[int, int, int] = (0, 0, 0),
        fontsize: int = 25,
    ) -> None:
        super().__init__(parent, width, height, x, y)
        self.text = text
        self.onclick = onclick
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.Font(None, fontsize)

    def on_mouse_left_click(self) -> None:
        self.onclick()

    def render(self) -> None:
        draw.rect(self.surface, self.color, pygame.Rect((0, 0, self.width, self.height)))
        rendered_text = self.font.render(self.text, True, self.text_color)
        xsize, ysize = rendered_text.get_size()
        self.surface.blit(rendered_text, (self.width // 2 - xsize // 2, self.height // 2 - ysize // 2))
