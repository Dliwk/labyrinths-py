"""Simple UI button widget."""

from typing import Callable

from labyrinths.ui import Widget
from labyrinths.ui.widgets.label import TextLabel


class Button(TextLabel):

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
        hovered_color: tuple[int, int, int] = (150, 150, 150),
        text_color: tuple[int, int, int] = (0, 0, 0),
        fontsize: int = 25,
    ) -> None:
        super().__init__(parent, width, height, x, y, text, color, text_color, fontsize)
        self.onclick = onclick
        self.normal_color = color
        self.hovered_color = hovered_color

    def on_mouse_left_click(self) -> None:
        self.onclick()

    def on_mouse_hover(self) -> None:
        self.color = self.hovered_color

    def on_mouse_hover_end(self) -> None:
        self.color = self.normal_color
