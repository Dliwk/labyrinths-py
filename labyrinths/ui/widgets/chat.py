"""Chat widget."""
from typing import Callable, Tuple

from typing_extensions import override
import pygame

from labyrinths.connection.client import ClientToHostConnection
from labyrinths.ui import Widget
from labyrinths.ui.widgets.button import Button
from labyrinths.ui.widgets.input import TextInput


class ChatWidget(Widget):
    """Simple chat widget."""

    def __init__(
            self,
            parent: Widget,
            width: int,
            height: int,
            x: int,
            y: int,
            connection: ClientToHostConnection,
    ) -> None:
        super().__init__(parent, width, height, x, y)
        self.surface.set_alpha(200)
        self.connection = connection
        self.text_input = TextInput(self, width - 20, 20, 0, height - 20)
        Button(self, 20, 20, width - 20, height - 20, text=">", onclick=self.send)
        self.messages: list[Tuple[str, str, Tuple[int, int, int]]] = []

        self.font = pygame.font.Font(None, 24)

    def put(self, message: str, name: str, color: Tuple[int, int, int]) -> None:
        self.messages.insert(0, (message, name, color))
        if len(self.messages) > 9:
            self.messages.pop()

    @override
    def on_keydown(self, key: int, event: pygame.Event) -> None:
        if self.text_input.hovered and key == pygame.K_RETURN:
            self.send()

    @override
    def render(self) -> None:
        ypos = self.height - 20
        for message, name, color in self.messages:
            rendered_text = self.font.render(f'{name}: {message}', True, color, wraplength=self.width)
            xsize, ysize = rendered_text.get_size()
            self.surface.blit(
                rendered_text, (0, ypos - ysize)
            )
            ypos -= ysize

    def send(self) -> None:
        self.connection.send_packet('game.client.chat', {'message': self.text_input.text})
        self.text_input.text = ''
