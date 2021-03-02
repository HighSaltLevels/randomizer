""" Module to init and create buttons """

from PyQt5.QtWidgets import QPushButton


def create_buttons(widget):
    """ Create all the push buttons """

    buttons = {
        "randomize": QPushButton("Randomize!", widget),
        "modify": QPushButton("Modify!", widget),
    }

    return buttons
