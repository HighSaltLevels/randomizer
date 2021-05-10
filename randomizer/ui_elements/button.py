""" Module to init and create buttons """

from PyQt5.QtWidgets import QPushButton

from controller import browse_handler, randomizer_handler


def create_buttons(parent):
    """ Create all the push buttons """

    buttons = {
        "randomize": QPushButton("Randomize!", parent),
        "browse": QPushButton("Browse Rom Path", parent),
    }

    buttons["browse"].clicked.connect(lambda: browse_handler(parent))
    buttons["randomize"].clicked.connect(lambda: randomizer_handler(parent))

    return buttons
