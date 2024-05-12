"""Simple Admin Panel."""

from typing import Callable

from labyrinths.session.clientsession import ClientSession
from labyrinths.ui import Widget
from labyrinths.ui.widgets.button import Button
from labyrinths.ui.widgets.container import Container


class AdminPanel(Container):
    """Simple Admin Panel."""

    def __init__(
        self,
        parent: Widget,
        width: int,
        height: int,
        x: int,
        y: int,
        session: ClientSession,
    ) -> None:
        super().__init__(parent, width, height, x, y)
        self.session = session
        Button(self, width, height, 0, 0, text="new", onclick=self.new_maze)

    def new_maze(self) -> None:
        self.session.admin_command("new_game", {"w": 10, "h": 10})
