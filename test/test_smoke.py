"""Smoke testing."""
import time
from threading import Thread

from labyrinths.connection.client import ClientToHostConnection
from labyrinths.connection.host import HostConnectionSet
from labyrinths.session.clientsession import ClientSession
from labyrinths.session.hostsession import HostSession
from labyrinths.ui.widgets.connectmenu import ConnectMenu
from labyrinths.ui.widgets.hostmenu import HostMenu
from ui_common import pygame_headless

from labyrinths.ui.mainwindow import MainWindow
from labyrinths.ui.widgets.mainmenu import MainMenu


def test_host_menu(pygame_headless) -> None:
    mainwindow = MainWindow(800, 600)
    main_menu = MainMenu(mainwindow.root_widget, mainwindow.width, mainwindow.height, 0, 0)
    host_menu = HostMenu(main_menu, main_menu.width, main_menu.height, 0, 0)
    host_menu.host_server()

    mainwindow.run(once=True)
    time.sleep(0.1)
    mainwindow.run(once=True)


def test_connect_menu(pygame_headless) -> None:
    # Spin up internal server.
    host = HostConnectionSet("127.0.0.1", 12301)
    host_session = HostSession(host)

    def run_server() -> None:
        while True:
            host.update()
            time.sleep(0.01)

    Thread(target=run_server, daemon=True).start()

    mainwindow = MainWindow(800, 600)
    main_menu = MainMenu(mainwindow.root_widget, mainwindow.width, mainwindow.height, 0, 0)
    connect_menu = ConnectMenu(main_menu, main_menu.width, main_menu.height, 0, 0)
    connect_menu.port_input.text = '12301'
    connect_menu.connect()

    mainwindow.run(once=True)
    time.sleep(0.5)
    mainwindow.run(once=True)


def test_chat(pygame_headless) -> None:
    # Spin up internal server.
    host = HostConnectionSet("127.0.0.1", 12302)
    host_session = HostSession(host)

    def run_server() -> None:
        while True:
            host.update()
            time.sleep(0.01)

    Thread(target=run_server, daemon=True).start()

    mainwindow = MainWindow(800, 600)
    connection = ClientToHostConnection("127.0.0.1", 12302)
    client_session = ClientSession(connection, mainwindow.root_widget)
    client_session.name = "tester"

    def run_client() -> None:
        nonlocal client_session
        while not client_session.dead:
            client_session.update()
            time.sleep(0.01)

    Thread(target=run_client, daemon=True).start()

    client_session.chat_widget.text = 'hello'
    client_session.chat_widget.send()

    mainwindow.run(once=True)
    time.sleep(0.5)
    mainwindow.run(once=True)
