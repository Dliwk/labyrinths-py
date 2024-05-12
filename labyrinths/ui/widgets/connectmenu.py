"""Connect menu."""

import logging
import time
from threading import Thread

from labyrinths.connection.client import ClientToHostConnection
from labyrinths.session.clientsession import ClientSession
from labyrinths.ui import Widget
from labyrinths.ui.widgets.button import Button
from labyrinths.ui.widgets.container import Container
from labyrinths.ui.widgets.input import TextInput
from labyrinths.ui.widgets.label import TextLabel

logger = logging.getLogger(__name__)


class ConnectMenu(Container):
    """Connect Menu."""

    def __init__(
        self,
        parent: Widget,
        width: int,
        height: int,
        x: int,
        y: int,
    ) -> None:
        super().__init__(parent, width, height, x, y)
        TextLabel(
            self,
            300,
            50,
            width // 2 - 150,
            80,
            text="Connect menu",
            color=(0, 0, 0),
            text_color=(0, 255, 0),
            fontsize=64,
        )
        TextLabel(self, 200, 30, width // 2 - 220, height // 2 - 60, text="enter host:")
        self.host_input = TextInput(self, 200, 30, width // 2 + 20, height // 2 - 60, text="127.0.0.1")

        TextLabel(self, 200, 30, width // 2 - 220, height // 2, text="enter port:")
        self.port_input = TextInput(self, 200, 30, width // 2 + 20, height // 2, text="12345", allowed="0123456789")

        TextLabel(self, 200, 30, width // 2 - 220, height // 2 + 60, text="name")
        self.name_input = TextInput(self, 200, 30, width // 2 + 20, height // 2 + 60, text="Player")

        Button(self, 100, 30, width // 2 - 50, height // 2 + 100, text="connect", onclick=self.connect)

        self.error_label = TextLabel(
            self, 400, 60, width // 2 - 200, height // 2 + 150, text="", color=(0, 0, 0), text_color=(255, 0, 0)
        )

    def connect(self) -> None:
        try:
            connection = ClientToHostConnection(self.host_input.text, int(self.port_input.text))
            assert self.parent is not None
            assert self.parent.parent is not None
            client_session = ClientSession(connection, self.parent.parent)
            client_session.name = self.name_input.text

            def run_client() -> None:
                nonlocal client_session
                while not client_session.dead:
                    client_session.update()
                    time.sleep(0.01)

            Thread(target=run_client, daemon=True).start()

            # Assuming parent is main menu
            self.parent.close()

        except Exception as e:
            self.error_label.text = str(e)
            logger.exception("Error connecting to host")
