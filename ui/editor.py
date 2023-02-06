from typing import List

from PySide6.QtWidgets import QMainWindow, QWidget, QGridLayout, QToolBar, QMenuBar, QGroupBox, QTableWidget, \
    QTableWidgetItem, QHeaderView

from parser.desktop_file import DesktopFileHandler, DesktopFile
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
        self.setMinimumSize(700, 800)

        # determine the current linux distro (todo: add try/except for when a distro isn't supported)
        self._current_distro = distro.get_distro()
        self.setWindowTitle(f"Desktop File Editor - {self._current_distro.value.title()}")

        # toolbar
        self.menubar = QMenuBar()
        file = self.menubar.addMenu("File")
        file_open = file.addAction("Open")
        file_save = file.addAction("Save")

        help = self.menubar.addMenu("Help")
        help_about = help.addAction("About")

        self.setMenuBar(self.menubar)

        # desktop file handler
        self._desktop_file_handler = DesktopFileHandler()

        # load the desktop files (only time this should happen)
        self._desktop_file_handler.load_desktop_files()

        # begin drawing UI
        self._selector = DesktopFileSelector()
        self._layout.addWidget(self._selector)

        # finished, load files
        self._load_files()

    def _load_files(self):
        """
        Called after the UI is done being drawn, loads the files
        :return:
        """
        self._selector.load_files(self._desktop_file_handler.get_desktop_files())


class DesktopFileSelector(QGroupBox):
    class _SelectorTable(QTableWidget):
        def __init__(self):
            super().__init__()
            self.setColumnCount(2)
            self.setHorizontalHeaderLabels(["Name", "ID"])
            self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
            self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

    def __init__(self):
        super().__init__(title="Desktop Files")
        self._layout = QGridLayout()
        self.setLayout(self._layout)

        self._table = self._SelectorTable()
        self._layout.addWidget(self._table)

    def load_files(self, desktop_files: List[DesktopFile]):
        """
        Loads the desktop files
        """
        self._table.setRowCount(0)
        for elem, file in enumerate(desktop_files):
            self._table.insertRow(elem)
            self._table.setItem(elem, 0, QTableWidgetItem(file.name))
            self._table.setItem(elem, 1, QTableWidgetItem(file.id))