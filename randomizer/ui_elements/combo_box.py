""" Module for generating all the combo boxes """

from PyQt5.QtWidgets import QComboBox

from constants import Hints, CLASS_MODE_OPTIONS
from controller import combo_box_handler
from config import CONFIG


def create_combo_boxes():
    """Init and return a dict of combo boxes"""

    class_mode = QComboBox()
    for option in CLASS_MODE_OPTIONS:
        class_mode.addItem(option)

    boxes = {
        "class_mode": class_mode,
    }

    boxes["class_mode"].setToolTip(Hints.CLASS_MODE)
    boxes["class_mode"].currentIndexChanged.connect(
        lambda: combo_box_handler(boxes["class_mode"].currentText())
    )
    boxes["class_mode"].setCurrentText(CONFIG["randomize"]["classes"]["mode"])
    return boxes
