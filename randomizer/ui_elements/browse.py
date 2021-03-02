""" Module for creating file browsers """

from PyQt5.QtWidgets import QFileDialog


def create_file_browsers(widget):
    """ Init and create all file browsers """
    file_browsers = {"rom_path": QFileDialog(widget, "Open Rom")}

    return file_browsers
