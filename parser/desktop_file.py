import os
from enum import Enum
from typing import List, Optional, Union

from loguru import logger
from pydantic import BaseModel

from util import distro


class DesktopFileType(Enum):
    APPLICATION = "Application"
    LINK = "Link"
    DIRECTORY = "Directory"


class DesktopFile(BaseModel):
    """
    These are the .desktop file key entries that are supported by this software currently, see the full list here:
    https://specifications.freedesktop.org/desktop-entry-spec/desktop-entry-spec-latest.html#basic-format
    """
    id: Optional[str] = None
    type: Optional[DesktopFileType] = None
    name: Optional[str] = None
    generic_name: Optional[str] = None
    no_display: Optional[bool] = None
    comment: Optional[str] = None
    icon: Optional[str] = None
    hidden: Optional[bool] = None
    try_exec: Optional[str] = None
    exec: Optional[str] = None
    path: Optional[str] = None
    terminal: Optional[bool] = None
    url: Optional[str] = None


class DesktopFileHandler:
    def __init__(self):
        self._desktop_files: List[DesktopFile] = []
        self._location = distro.get_desktop_file_directory()

    def load_desktop_files(self):
        """
        Clears the stored desktop files and reloads the list
        :return:
        """
        self._desktop_files = []
        files = os.listdir(distro.get_desktop_file_directory().value)

        # iterate over the files, ensure their extensions are .desktop and load them into DesktopFile objects
        for file in files:
            if ".desktop" in file:
                desktop_file = self._parse_file(file)
                if desktop_file:
                    self._desktop_files.append(desktop_file)
            else:
                logger.warning(f"'{file}' does not appear to be a .desktop file, and will be ignored")

    def get_desktop_files(self) -> List[DesktopFile]:
        return self._desktop_files

    def _parse_file(self, filename: str) -> Union[DesktopFile, None]:
        """
        Parses a .desktop file, returns a DesktopFile object
        :param filename:
        :return:
        """
        blacklist_characters = ["[Desktop", "#", "\n"]
        desktop_file = DesktopFile()

        # read the file
        with open(os.path.join(distro.get_desktop_file_directory().value, filename), "r") as f:
            file = f.read().split("\n")

        # iterate over each line,
        for elem, line in enumerate(file):
            # set id
            desktop_file.id = filename

            # if this isn't a key/value pair, skip this line
            if any([char in line for char in blacklist_characters]) or not line:
                continue

            # if it is a key/value pair, split it and continue
            try:
                key, value = line.split("=")
            except ValueError as e:
                logger.critical(f"Unknown format: '{line}': Line# {elem} in {filename}")
                continue

            # begin populating object
            if key == "Name":
                desktop_file.name = value
            elif key == "Type":
                desktop_file.type = DesktopFileType(value)
            elif key == "GenericName":
                desktop_file.generic_name = value
            elif key == "NoDisplay":
                desktop_file.no_display = value
            elif key == "Comment":
                desktop_file.comment = value
            elif key == "Icon":
                desktop_file.icon = value
            elif key == "Hidden":
                desktop_file.hidden = bool(value)
            elif key == "TryExec":
                desktop_file.try_exec = value
            elif key == "Exec":
                desktop_file.exec = value
            elif key == "Path":
                desktop_file.path = value
            elif key == "Terminal":
                desktop_file.terminal = bool(value)
            elif key == "URL":
                desktop_file.url = value

        # warn if the file does not have a valid Name key
        if not desktop_file.name:
            logger.warning(f"'{filename}' does not have a valid 'Name' key & therefore is not a valid .desktop file, skipping!")
            return

        return desktop_file




