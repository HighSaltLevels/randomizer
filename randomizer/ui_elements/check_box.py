""" Module for generating all check boxes """

from PyQt5.QtWidgets import QCheckBox


def create_check_boxes():
    """ Init and return a dict of check boxes """
    boxes = [
        "pb_enabled",
        "bb_enabled",
        "ob_enabled",
        "cb_enabled",
        "master_seal_enabled",
        "pg_enabled",
        "bg_enabled",
        "og_enabled",
        "mpb_enabled",
        "mbb_enabled",
        "mob_enabled",
        "mpg_enabled",
        "mbg_enabled",
        "mog_enabled",
    ]

    return {box: QCheckBox("Enabled") for box in boxes}
