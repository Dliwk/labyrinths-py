"""Simple UI text input widget."""

import pygame
from pygame import draw

from labyrinths.ui import Widget


class TextInput(Widget):
    """A simple text input widget."""

    def __init__(
        self,
        parent: Widget,
        width: int,
        height: int,
        x: int,
        y: int,
        text: str = "",
        allowed: str | None = None,
        color: tuple[int, int, int] = (180, 180, 180),
        inner_color: tuple[int, int, int] = (220, 220, 220),
        text_color: tuple[int, int, int] = (0, 0, 0),
        fontsize: int = 25,
    ) -> None:
        super().__init__(parent, width, height, x, y)
        self.text = text
        self.color = color
        self.inner_color = inner_color
        self.text_color = text_color
        self.font = pygame.font.Font(None, fontsize)
        self.hovered = False
        self.allowed = allowed

    def on_mouse_hover(self) -> None:
        self.hovered = True

    def on_mouse_hover_end(self) -> None:
        self.hovered = False

    def render(self) -> None:
        draw.rect(self.surface, self.color, pygame.Rect((0, 0, self.width, self.height)))
        draw.rect(self.surface, self.inner_color, pygame.Rect((4, 4, self.width - 8, self.height - 8)))

        text = self.text
        if self.hovered:
            text += "_"

        rendered_text = self.font.render(text, True, self.text_color)
        xsize, ysize = rendered_text.get_size()
        self.surface.blit(rendered_text, (self.width // 2 - xsize // 2, self.height // 2 - ysize // 2))

    def on_keydown(self, key: int, event: pygame.Event) -> None:
        if not self.hovered:
            return
        if key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
        elif event.unicode.isprintable():
            if self.allowed is None or event.unicode in self.allowed:
                self.text += event.unicode
