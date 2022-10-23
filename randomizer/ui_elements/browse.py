""" Module for file browsers """

from PyQt5.QtWidgets import QFileDialog


def create_file_browser(parent):
    """Create a file browser that sets a line_edit"""

    browser = QFileDialog(parent)
    browser.setFileMode(QFileDialog.AnyFile)

    return browser
