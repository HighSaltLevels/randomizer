""" Module for generating all the combo boxes """

from PyQt5.QtWidgets import QComboBox


def create_combo_boxes():
    """ Init and return a dict of combo boxes """

    class_mode = QComboBox()
    class_mode.addItem("Combat (Units Guaranteed To Have Offense)")
    class_mode.addItem("Combat/Staff (Some Units May Wield Only Staves)")
    class_mode.addItem("All (All classes are randomized")

    boxes = {
        "class_mode": class_mode,
    }

    return boxes
