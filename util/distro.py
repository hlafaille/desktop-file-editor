import os
from enum import Enum

# todo add more distro support here!


class SupportedDistro(Enum):
    ARCH = "arch"


class DesktopFileLocation(Enum):
    ARCH = os.path.join("/usr", "share", "applications")


def get_desktop_file_directory() -> DesktopFileLocation:
    """
    Gets the desktop file directory for this distro
    :return:
    """
    return DesktopFileLocation[get_distro().value.upper()]


def get_distro() -> SupportedDistro:
    """
    Gets which distro is currently running
    :return:
    """
    with open(os.path.join("/etc", "os-release")) as f:
        os_release = f.read().split("\n")

    for line in os_release:
        if line[0:2] == "ID":
            return SupportedDistro(line[3:len(line)])

    raise ValueError(f"Unsupported distribution")
