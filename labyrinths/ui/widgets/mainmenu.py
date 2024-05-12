"""Main menu."""

import random
import time
from threading import Thread

from labyrinths.connection.client import ClientToHostConnection
from labyrinths.connection.host import HostConnectionSet
from labyrinths.session.clientsession import ClientSession
from labyrinths.session.hostsession import HostSession
from labyrinths.ui import Widget
from labyrinths.ui.widgets.adminpanel import AdminPanel
from labyrinths.ui.widgets.button import Button
from labyrinths.ui.widgets.connectmenu import ConnectMenu
from labyrinths.ui.widgets.container import Container
from labyrinths.ui.widgets.label import TextLabel


class MainMenu(Container):
    """Simple Main Menu."""

    def __init__(
            self,
            parent: Widget,
            width: int,
            height: int,
            x: int,
            y: int,
            message: str = "",
    ) -> None:
        super().__init__(parent, width, height, x, y)
        TextLabel(
            self, 300, 50, width // 2 - 150, 80, text="Main menu", color=(0, 0, 0), text_color=(0, 255, 0), fontsize=64
        )
        self.host_button = Button(self, 80, 30, width // 2 - 40, height // 2 - 60, text="host",
                                  onclick=self.host_server)
        self.show_connect_menu_button = Button(self, 80, 30, width // 2 - 40, height // 2 - 20, text="connect",
                                               onclick=self.show_connect_menu)

        TextLabel(
            self,
            300,
            50,
            width // 2 - 150,
            height - 80,
            text=message,
            color=(0, 0, 0),
            text_color=(255, 0, 0),
            fontsize=32,
        )

    def show_connect_menu(self):
        ConnectMenu(self, self.width, self.height, 0, 0)

    def host_server(self, port: int | None = None) -> None:
        if port is None:
            port = random.randint(10000, 20000)

        # Spin up internal server.
        host = HostConnectionSet("0.0.0.0", port)
        host_session = HostSession(host)

        def run_server() -> None:
            while True:
                host.update()
                time.sleep(0.01)

        Thread(target=run_server, daemon=True).start()

        # Connect to it.
        assert self.parent is not None
        cont = Container(self.parent, self.parent.width, self.parent.height, 0, 0)

        connection = ClientToHostConnection("127.0.0.1", port)
        client_session = ClientSession(connection, cont)
        host_session.admin_ids.append(1)

        def run_client() -> None:
            nonlocal client_session
            while True:
                client_session.update()
                time.sleep(0.01)

        Thread(target=run_client, daemon=True).start()

        AdminPanel(cont, 50, 30, self.width - 50, self.height - 60, client_session)

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
        self.close()
