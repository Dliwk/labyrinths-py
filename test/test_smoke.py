"""Smoke testing."""

from labyrinths.ui.widgets.connectmenu import ConnectMenu
from labyrinths.ui.widgets.mainmenu import MainMenu
from ui_common import pygame_headless

from labyrinths.ui.mainwindow import MainWindow


def test_main_menu_and_internal_server(pygame_headless) -> None:
    mainwindow = MainWindow(800, 600)
    main_menu = MainMenu(mainwindow.root_widget, mainwindow.width, mainwindow.height, 0, 0)

    main_menu.host_button.onclick()


def test_connect_menu(pygame_headless) -> None:
    mainwindow = MainWindow(800, 600)
    main_menu = MainMenu(mainwindow.root_widget, mainwindow.width, mainwindow.height, 0, 0)

    main_menu.host_server(13373)

    mainwindow = MainWindow(800, 600)
    main_menu = MainMenu(mainwindow.root_widget, mainwindow.width, mainwindow.height, 0, 0)
    connect_menu = ConnectMenu(main_menu, main_menu.width, main_menu.height, 0, 0)
    connect_menu.port_input.text = '13373'
    connect_menu.connect()
