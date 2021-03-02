""" Module for generating all the combo boxes """

from PyQt5.QtWidgets import QComboBox

from constants import Hints


def create_combo_boxes():
    """ Init and return a dict of combo boxes """

    class_mode = QComboBox()
    class_mode.addItem("Combat")
    class_mode.addItem("Combat/Staff")
    class_mode.addItem("All")

    boxes = {
        "class_mode": class_mode,
    }

    boxes["class_mode"].setToolTip(Hints.CLASS_MODE)

    return boxes
