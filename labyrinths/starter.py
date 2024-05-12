import random
import time
from threading import Thread

import coloredlogs

from labyrinths.connection.client import ClientToHostConnection
from labyrinths.connection.host import HostConnectionSet
from labyrinths.session.clientsession import ClientSession
from labyrinths.session.hostsession import HostSession
from labyrinths.ui.mainwindow import MainWindow
from labyrinths.ui.widgets.adminpanel import AdminPanel
from labyrinths.ui.widgets.mainmenu import MainMenu

coloredlogs.install(level="DEBUG")


def main():
    ui = MainWindow(800, 600)
    MainMenu(ui.root_widget, ui.width, ui.height, 0, 0)

    ui.run()
