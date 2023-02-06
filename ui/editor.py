from PySide6.QtWidgets import QMainWindow, QWidget, QGridLayout, QToolBar, QMenuBar

from parser.desktop_file import DesktopFileHandler
from util import distro


class Editor(QMainWindow):
    """The main editor"""

    def __init__(self):
        super().__init__()

        # window setup
        self._widget = QWidget()
        self._layout = QGridLayout()
        self._widget.setLayout(self._layout)
        self.setCentralWidget(self._widget)
        self.setMinimumSize(600, 800)

        # determine the current linux distro
        self._current_distro = distro.get_distro()

        self.setWindowTitle(f"Desktop File Editor - {self._current_distro.value.title()}")

        # toolbar
        self.menubar = QMenuBar()
        file = self.menubar.addMenu("File")
        file_open = file.addMenu("Open")
        file_save = file.addMenu("Save")

        help = self.menubar.addMenu("Help")
        help_about = help.addMenu("About")

        self.setMenuBar(self.menubar)

        # desktop file handler
        self._desktop_file_handler = DesktopFileHandler()

        # load the desktop files (only time this should happen)
        self._desktop_file_handler.load_desktop_files()