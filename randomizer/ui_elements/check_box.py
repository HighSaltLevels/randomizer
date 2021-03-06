""" Module for generating all check boxes """

from PyQt5.QtWidgets import QCheckBox

from constants import Hints
from controllers import check_box_controller


def create_check_boxes(spin_boxes):
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

    for check_box in mapping.values():
        check_box.setChecked(True)

    mapping["pb_enabled"].setToolTip(Hints.PLAYABLE_BASES)
    mapping["pb_enabled"].stateChanged.connect(lambda: check_box_controller.handler(spin_boxes["pb_min"], spin_boxes["pb_max"]))

    mapping["bb_enabled"].setToolTip(Hints.BOSS_BASES)
    mapping["bb_enabled"].stateChanged.connect(lambda: check_box_controller.handler(spin_boxes["bb_min"], spin_boxes["bb_max"]))

    mapping["ob_enabled"].setToolTip(Hints.OTHER_BASES)
    mapping["ob_enabled"].stateChanged.connect(lambda: check_box_controller.handler(spin_boxes["ob_min"], spin_boxes["ob_max"]))

    mapping["cb_enabled"].setToolTip(Hints.CLASS_BASES)
    mapping["cb_enabled"].stateChanged.connect(lambda: check_box_controller.handler(spin_boxes["cb_min"], spin_boxes["cb_max"]))

    mapping["pg_enabled"].setToolTip(Hints.PLAYABLE_GROWTHS)
    mapping["pg_enabled"].stateChanged.connect(lambda: check_box_controller.handler(spin_boxes["pg_min"], spin_boxes["pg_max"]))

    mapping["bg_enabled"].setToolTip(Hints.BOSS_GROWTHS)
    mapping["bg_enabled"].stateChanged.connect(lambda: check_box_controller.handler(spin_boxes["bg_min"], spin_boxes["bg_max"]))

    mapping["og_enabled"].setToolTip(Hints.OTHER_GROWTHS)
    mapping["og_enabled"].stateChanged.connect(lambda: check_box_controller.handler(spin_boxes["og_min"], spin_boxes["og_max"]))

    mapping["mpb_enabled"].setToolTip(Hints.MOD_PLAYABLE_BASES)
    mapping["mpb_enabled"].stateChanged.connect(lambda: check_box_controller.handler(spin_boxes["pb_mod"]))

    mapping["mbb_enabled"].setToolTip(Hints.MOD_BOSS_BASES)
    mapping["mbb_enabled"].stateChanged.connect(lambda: check_box_controller.handler(spin_boxes["bb_mod"]))

    mapping["mob_enabled"].setToolTip(Hints.MOD_OTHER_BASES)
    mapping["mob_enabled"].stateChanged.connect(lambda: check_box_controller.handler(spin_boxes["ob_mod"]))

    mapping["mpg_enabled"].setToolTip(Hints.MOD_PLAYABLE_GROWTHS)
    mapping["mpg_enabled"].stateChanged.connect(lambda: check_box_controller.handler(spin_boxes["pg_mod"]))

    mapping["mbg_enabled"].setToolTip(Hints.MOD_BOSS_GROWTHS)
    mapping["mbg_enabled"].stateChanged.connect(lambda: check_box_controller.handler(spin_boxes["bg_mod"]))

    mapping["mog_enabled"].setToolTip(Hints.MOD_OTHER_GROWTHS)
    mapping["mog_enabled"].stateChanged.connect(lambda: check_box_controller.handler(spin_boxes["og_mod"]))

    mapping["master_seal_enabled"].setToolTip(Hints.FORCE_MASTER_SEAL)

    return mapping
