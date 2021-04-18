""" Module to init and create buttons """

from PyQt5.QtWidgets import QPushButton

from controller import browse_handler


def create_buttons(widget, file_browser, line_edit):
    """ Create all the push buttons """

    buttons = {
        "randomize": QPushButton("Randomize!", widget),
        "browse": QPushButton("Browse Rom Path", widget),
    }

    buttons["browse"].clicked.connect(lambda: browse_handler(file_browser, line_edit))

    return buttons
