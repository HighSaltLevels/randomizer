""" Module for creating all teh spin boxes """
from PyQt5.QtWidgets import QSpinBox

from constants import NORMAL_FONT


def create_spin_boxes(widget):
    """ Init and return a dict of line edits """

    min_max_spin_boxes = {
        "pb_min": QSpinBox(widget),
        "pb_max": QSpinBox(widget),
        "bb_min": QSpinBox(widget),
        "bb_max": QSpinBox(widget),
        "ob_min": QSpinBox(widget),
        "ob_max": QSpinBox(widget),
        "cb_min": QSpinBox(widget),
        "cb_max": QSpinBox(widget),
        "pg_min": QSpinBox(widget),
        "pg_max": QSpinBox(widget),
        "bg_min": QSpinBox(widget),
        "bg_max": QSpinBox(widget),
        "og_min": QSpinBox(widget),
        "og_max": QSpinBox(widget),
    }
    for spin_box in min_max_spin_boxes.values():
        spin_box.setFont(NORMAL_FONT)
        spin_box.setRange(0, 255)

    mod_spin_boxes = {
        "pb_mod": QSpinBox(widget),
        "bb_mod": QSpinBox(widget),
        "ob_mod": QSpinBox(widget),
        "pg_mod": QSpinBox(widget),
        "bg_mod": QSpinBox(widget),
        "og_mod": QSpinBox(widget),
    }

    for spin_box in mod_spin_boxes.values():
        spin_box.setFont(NORMAL_FONT)
        spin_box.setRange(-100, 100)

    spin_boxes = min_max_spin_boxes
    spin_boxes.update(mod_spin_boxes)

    return spin_boxes
