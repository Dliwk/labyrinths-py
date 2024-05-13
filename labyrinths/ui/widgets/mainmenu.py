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
from labyrinths.ui.widgets.hostmenu import HostMenu
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
        self.host_button = Button(
            self, 80, 30, width // 2 - 40, height // 2 - 60, text="host", onclick=self.show_host_menu
        )
        self.show_connect_menu_button = Button(
            self, 80, 30, width // 2 - 40, height // 2 - 20, text="connect", onclick=self.show_connect_menu
        )

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

    def show_host_menu(self):
        HostMenu(self, self.width, self.height, 0, 0)
