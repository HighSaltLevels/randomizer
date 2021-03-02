""" Module for generating all check boxes """

from PyQt5.QtWidgets import QCheckBox

from constants import Hints


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

    mapping = {box: QCheckBox("Enabled") for box in boxes}

    mapping["pb_enabled"].setToolTip(Hints.PLAYABLE_BASES)
    mapping["bb_enabled"].setToolTip(Hints.BOSS_BASES)
    mapping["ob_enabled"].setToolTip(Hints.OTHER_BASES)
    mapping["cb_enabled"].setToolTip(Hints.CLASS_BASES)

    mapping["pg_enabled"].setToolTip(Hints.PLAYABLE_GROWTHS)
    mapping["bg_enabled"].setToolTip(Hints.BOSS_GROWTHS)
    mapping["og_enabled"].setToolTip(Hints.OTHER_GROWTHS)

    mapping["mpb_enabled"].setToolTip(Hints.MOD_PLAYABLE_BASES)
    mapping["mbb_enabled"].setToolTip(Hints.MOD_BOSS_BASES)
    mapping["mob_enabled"].setToolTip(Hints.MOD_OTHER_BASES)

    mapping["mpg_enabled"].setToolTip(Hints.MOD_PLAYABLE_GROWTHS)
    mapping["mbg_enabled"].setToolTip(Hints.MOD_BOSS_GROWTHS)
    mapping["mog_enabled"].setToolTip(Hints.MOD_OTHER_GROWTHS)

    mapping["master_seal_enabled"].setToolTip(Hints.FORCE_MASTER_SEAL)

    return mapping
