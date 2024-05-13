"""Smoke testing."""

import random
import time
from threading import Thread

import pytest
from ui_common import pygame_headless

from labyrinths.connection.client import ClientToHostConnection
from labyrinths.connection.host import HostConnectionSet
from labyrinths.session.clientsession import ClientSession
from labyrinths.session.hostsession import HostSession
from labyrinths.ui.mainwindow import MainWindow
from labyrinths.ui.widgets.connectmenu import ConnectMenu
from labyrinths.ui.widgets.hostmenu import HostMenu
from labyrinths.ui.widgets.mainmenu import MainMenu


@pytest.fixture
def random_port():
    return random.randint(10000, 20000)


def test_host_menu(pygame_headless) -> None:
    mainwindow = MainWindow(800, 600)
    main_menu = MainMenu(mainwindow.root_widget, mainwindow.width, mainwindow.height, 0, 0)
    host_menu = HostMenu(main_menu, main_menu.width, main_menu.height, 0, 0)
    host_menu.host_server()

    mainwindow.run(once=True)
    time.sleep(0.1)
    mainwindow.run(once=True)


def test_connect_menu(pygame_headless, random_port) -> None:
    # Spin up internal server.
    host = HostConnectionSet("127.0.0.1", random_port)
    host_session = HostSession(host)

    def run_server() -> None:
        while True:
            host.update()
            time.sleep(0.01)

    Thread(target=run_server, daemon=True).start()

    mainwindow = MainWindow(800, 600)
    main_menu = MainMenu(mainwindow.root_widget, mainwindow.width, mainwindow.height, 0, 0)
    connect_menu = ConnectMenu(main_menu, main_menu.width, main_menu.height, 0, 0)
    connect_menu.port_input.text = str(random_port)
    connect_menu.connect()

    mainwindow.run(once=True)
    time.sleep(0.5)
    mainwindow.run(once=True)


def test_chat(pygame_headless, random_port) -> None:
    # Spin up internal server.
    host = HostConnectionSet("127.0.0.1", random_port)
    host_session = HostSession(host)

    def run_server() -> None:
        while True:
            host.update()
            time.sleep(0.01)

    Thread(target=run_server, daemon=True).start()

    mainwindow = MainWindow(800, 600)
    connection = ClientToHostConnection("127.0.0.1", random_port)
    client_session = ClientSession(connection, mainwindow.root_widget)
    client_session.name = "tester"

    def run_client() -> None:
        nonlocal client_session
        while not client_session.dead:
            client_session.update()
            time.sleep(0.01)

    Thread(target=run_client, daemon=True).start()

    client_session.chat_widget.text_input.text = "hello"
    client_session.chat_widget.send()

    mainwindow.run(once=True)
    time.sleep(0.5)
    mainwindow.run(once=True)
