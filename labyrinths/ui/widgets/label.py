"""Simple UI text label widget."""

import pygame
from pygame import draw

from labyrinths.ui import Widget


class TextLabel(Widget):
    """A simple text label widget."""

    def __init__(
        self,
        parent: Widget,
        width: int,
        height: int,
        x: int,
        y: int,
        text: str = "button",
        color: tuple[int, int, int] = (200, 200, 200),
        text_color: tuple[int, int, int] = (0, 0, 0),
        fontsize: int = 25,
    ) -> None:
        super().__init__(parent, width, height, x, y)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.Font(None, fontsize)

    def render(self) -> None:
        draw.rect(self.surface, self.color, pygame.Rect((0, 0, self.width, self.height)))
        lines = self.text.splitlines()
        for i, line in enumerate(reversed(lines)):
            rendered_text = self.font.render(line, True, self.text_color)
            xsize, ysize = rendered_text.get_size()
            self.surface.blit(
                rendered_text, (self.width // 2 - xsize // 2, self.height // 2 - ysize - ysize * (i - len(lines) / 2))
            )
