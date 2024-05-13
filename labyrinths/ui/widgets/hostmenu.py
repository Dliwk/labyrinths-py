"""Host game menu."""

import logging
import time
from threading import Thread

from labyrinths.connection.client import ClientToHostConnection
from labyrinths.connection.host import HostConnectionSet
from labyrinths.session.clientsession import ClientSession
from labyrinths.session.hostsession import HostSession
from labyrinths.ui import Widget
from labyrinths.ui.widgets.adminpanel import AdminPanel
from labyrinths.ui.widgets.button import Button
from labyrinths.ui.widgets.container import Container
from labyrinths.ui.widgets.input import TextInput
from labyrinths.ui.widgets.label import TextLabel

logger = logging.getLogger(__name__)


class HostMenu(Container):
    """Host game Menu."""

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
            self.width,
            50,
            0,
            80,
            text="Host menu",
            color=(0, 0, 0),
            text_color=(0, 255, 0),
            fontsize=64,
        )

        TextLabel(self, 200, 30, width // 2 - 220, height // 2 - 60, text="enter host:")
        self.host_input = TextInput(self, 200, 30, width // 2 + 20, height // 2 - 60, text="0.0.0.0")

        TextLabel(self, 200, 30, width // 2 - 220, height // 2, text="enter port:")
        self.port_input = TextInput(self, 200, 30, width // 2 + 20, height // 2, text="12345", allowed="0123456789")

        TextLabel(self, 200, 30, width // 2 - 220, height // 2 + 60, text="name")
        self.name_input = TextInput(self, 200, 30, width // 2 + 20, height // 2 + 60, text="Admin")

        Button(self, 100, 30, width // 2 - 50, height // 2 + 100, text="host", onclick=self.host_server)

        Button(self, 60, 30, width // 2 - 30, height - 80, text="back", onclick=self.close)

        self.error_label = TextLabel(
            self, 400, 60, width // 2 - 200, height // 2 + 150, text="", color=(0, 0, 0), text_color=(255, 0, 0)
        )

    def host_server(self) -> None:
        try:
            # Spin up internal server.
            port = int(self.port_input.text)
            host = HostConnectionSet(self.host_input.text, port)
            host_session = HostSession(host)

            def run_server() -> None:
                while True:
                    host.update()
                    time.sleep(0.01)

            Thread(target=run_server, daemon=True).start()

            # Connect to it.
            assert self.parent is not None
            assert self.parent.parent is not None
            cont = Container(self.parent.parent, self.parent.parent.width, self.parent.parent.height, 0, 0)

            connection = ClientToHostConnection("127.0.0.1", port)
            client_session = ClientSession(connection, cont)
            client_session.name = self.name_input.text
            host_session.admin_ids.append(1)

            def run_client() -> None:
                nonlocal client_session
                while True:
                    client_session.update()
                    time.sleep(0.01)

            Thread(target=run_client, daemon=True).start()

            admin_panel = AdminPanel(cont, 50, 30, self.width - 50, self.height - 60, client_session)
            admin_panel.new_maze()

            TextLabel(
                cont,
                100,
                30,
                self.width - 100,
                self.height - 30,
                text=f"port: {port}",
                color=(0, 0, 0),
                text_color=(0, 255, 0),
            )
            self.parent.close()
        except Exception as e:
            logger.exception("Exception in Host menu")
            self.error_label.text = str(e)
