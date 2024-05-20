import coloredlogs

from labyrinths.ui.mainwindow import MainWindow
from labyrinths.ui.widgets.mainmenu import MainMenu

coloredlogs.install(level="INFO")


def main():
    ui = MainWindow(800, 600)
    MainMenu(ui.root_widget, ui.width, ui.height, 0, 0)

    ui.run()
