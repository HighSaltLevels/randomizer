""" Module for generating all check boxes """

from PyQt5.QtWidgets import QCheckBox

from constants import Hints
from controller import handler
from config import CONFIG


def _set_configs(check_boxes, spin_boxes):
    """ Set the check box states based on the incoming config """
    base_configs = CONFIG["randomize"]["stats"]["bases"]
    check_boxes["pb_enabled"].setChecked(base_configs["playable"]["enabled"])
    spin_boxes["pb_min"].setDisabled(not base_configs["playable"]["enabled"])
    spin_boxes["pb_max"].setDisabled(not base_configs["playable"]["enabled"])

    check_boxes["bb_enabled"].setChecked(base_configs["boss"]["enabled"])
    spin_boxes["bb_min"].setDisabled(not base_configs["boss"]["enabled"])
    spin_boxes["bb_max"].setDisabled(not base_configs["boss"]["enabled"])

    check_boxes["ob_enabled"].setChecked(base_configs["other"]["enabled"])
    spin_boxes["ob_min"].setDisabled(not base_configs["other"]["enabled"])
    spin_boxes["ob_max"].setDisabled(not base_configs["other"]["enabled"])

    check_boxes["cb_enabled"].setChecked(base_configs["class"]["enabled"])
    spin_boxes["cb_min"].setDisabled(not base_configs["class"]["enabled"])
    spin_boxes["cb_max"].setDisabled(not base_configs["class"]["enabled"])

    growth_configs = CONFIG["randomize"]["stats"]["growths"]
    check_boxes["pg_enabled"].setChecked(growth_configs["playable"]["enabled"])
    spin_boxes["pg_min"].setDisabled(not growth_configs["playable"]["enabled"])
    spin_boxes["pg_max"].setDisabled(not growth_configs["playable"]["enabled"])

    check_boxes["bg_enabled"].setChecked(growth_configs["boss"]["enabled"])
    spin_boxes["bg_min"].setDisabled(not growth_configs["boss"]["enabled"])
    spin_boxes["bg_max"].setDisabled(not growth_configs["boss"]["enabled"])

    check_boxes["og_enabled"].setChecked(growth_configs["other"]["enabled"])
    spin_boxes["og_min"].setDisabled(not growth_configs["other"]["enabled"])
    spin_boxes["og_max"].setDisabled(not growth_configs["other"]["enabled"])

    base_configs = CONFIG["modify"]["stats"]["bases"]
    check_boxes["mpb_enabled"].setChecked(base_configs["playable"]["enabled"])
    spin_boxes["pb_mod"].setDisabled(not base_configs["playable"]["enabled"])

    check_boxes["mbb_enabled"].setChecked(base_configs["boss"]["enabled"])
    spin_boxes["bb_mod"].setDisabled(not base_configs["boss"]["enabled"])

    check_boxes["mob_enabled"].setChecked(base_configs["other"]["enabled"])
    spin_boxes["ob_mod"].setDisabled(not base_configs["other"]["enabled"])

    growth_configs = CONFIG["modify"]["stats"]["growths"]
    check_boxes["mpg_enabled"].setChecked(growth_configs["playable"]["enabled"])
    spin_boxes["pg_mod"].setDisabled(not growth_configs["playable"]["enabled"])

    check_boxes["mbg_enabled"].setChecked(growth_configs["boss"]["enabled"])
    spin_boxes["bg_mod"].setDisabled(not growth_configs["boss"]["enabled"])

    check_boxes["mog_enabled"].setChecked(growth_configs["other"]["enabled"])
    spin_boxes["og_mod"].setDisabled(not growth_configs["other"]["enabled"])

    check_boxes["master_seal_enabled"].setChecked(
        CONFIG["randomize"]["classes"]["all_master_seals"]["enabled"]
    )

    check_boxes["mix_promotes"].setChecked(
        CONFIG["randomize"]["mix_promotes"]["enabled"]
    )

    class_config = CONFIG["randomize"]["classes"]
    check_boxes["playable_class"].setChecked(class_config["playable"]["enabled"])
    check_boxes["boss_class"].setChecked(class_config["boss"]["enabled"])
    check_boxes["other_class"].setChecked(class_config["other"]["enabled"])


def create_check_boxes(parent):
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

    mapping["master_seal_enabled"].setToolTip(Hints.FORCE_MASTER_SEAL)
    mapping["master_seal_enabled"].stateChanged.connect(
        lambda: handler(
            "randomize/classes/all_master_seals",
            {"check_box": mapping["master_seal_enabled"]},
        )
    )

    mapping["playable_class"] = QCheckBox("Playable Classes")
    mapping["playable_class"].setToolTip(Hints.PLAYABLE_CLASSES)
    mapping["playable_class"].stateChanged.connect(
        lambda: handler(
            "randomizer/classes/playable", {"check_box": mapping["playable_class"]}
        )
    )

    mapping["boss_class"] = QCheckBox("Boss Classes")
    mapping["boss_class"].setToolTip(Hints.BOSS_CLASSES)
    mapping["boss_class"].stateChanged.connect(
        lambda: handler("randomizer/classes/boss", {"check_box": mapping["boss_class"]})
    )

    mapping["other_class"] = QCheckBox("Other Classes")
    mapping["other_class"].setToolTip(Hints.OTHER_CLASSES)
    mapping["other_class"].stateChanged.connect(
        lambda: handler(
            "randomizer/classes/other", {"check_box": mapping["other_class"]}
        )
    )

    mapping["mix_promotes"] = QCheckBox("Mix Promotes")
    mapping["mix_promotes"].setToolTip(Hints.MIX_PROMOTES)
    mapping["mix_promotes"].stateChanged.connect(
        lambda: handler(
            "randomize/mix_promotes", {"check_box": mapping["mix_promotes"]}
        )
    )

    mapping["pb_enabled"].setToolTip(Hints.PLAYABLE_BASES)
    mapping["pb_enabled"].stateChanged.connect(
        lambda: handler(
            "randomize/stats/bases/playable",
            {
                "spin_boxes": [
                    parent.spin_boxes["pb_min"],
                    parent.spin_boxes["pb_max"],
                ],
                "check_box": mapping["pb_enabled"],
            },
        )
    )

    mapping["bb_enabled"].setToolTip(Hints.BOSS_BASES)
    mapping["bb_enabled"].stateChanged.connect(
        lambda: handler(
            "randomize/stats/bases/boss",
            {
                "spin_boxes": [
                    parent.spin_boxes["bb_min"],
                    parent.spin_boxes["bb_max"],
                ],
                "check_box": mapping["bb_enabled"],
            },
        )
    )

    mapping["ob_enabled"].setToolTip(Hints.OTHER_BASES)
    mapping["ob_enabled"].stateChanged.connect(
        lambda: handler(
            "randomize/stats/bases/other",
            {
                "spin_boxes": [
                    parent.spin_boxes["ob_min"],
                    parent.spin_boxes["ob_max"],
                ],
                "check_box": mapping["ob_enabled"],
            },
        )
    )

    mapping["cb_enabled"].setToolTip(Hints.CLASS_BASES)
    mapping["cb_enabled"].stateChanged.connect(
        lambda: handler(
            "randomize/stats/bases/class",
            {
                "spin_boxes": [
                    parent.spin_boxes["cb_min"],
                    parent.spin_boxes["cb_max"],
                ],
                "check_box": mapping["cb_enabled"],
            },
        )
    )

    mapping["pg_enabled"].setToolTip(Hints.PLAYABLE_GROWTHS)
    mapping["pg_enabled"].stateChanged.connect(
        lambda: handler(
            "randomize/stats/growths/playable",
            {
                "spin_boxes": [
                    parent.spin_boxes["pg_min"],
                    parent.spin_boxes["pg_max"],
                ],
                "check_box": mapping["pg_enabled"],
            },
        )
    )

    mapping["bg_enabled"].setToolTip(Hints.BOSS_GROWTHS)
    mapping["bg_enabled"].stateChanged.connect(
        lambda: handler(
            "randomize/stats/growths/boss",
            {
                "spin_boxes": [
                    parent.spin_boxes["bg_min"],
                    parent.spin_boxes["bg_max"],
                ],
                "check_box": mapping["bg_enabled"],
            },
        )
    )

    mapping["og_enabled"].setToolTip(Hints.OTHER_GROWTHS)
    mapping["og_enabled"].stateChanged.connect(
        lambda: handler(
            "randomize/stats/growths/other",
            {
                "spin_boxes": [
                    parent.spin_boxes["og_min"],
                    parent.spin_boxes["og_max"],
                ],
                "check_box": mapping["og_enabled"],
            },
        )
    )

    mapping["mpb_enabled"].setToolTip(Hints.MOD_PLAYABLE_BASES)
    mapping["mpb_enabled"].stateChanged.connect(
        lambda: handler(
            "modify/stats/bases/playable",
            {
                "spin_boxes": [parent.spin_boxes["pb_mod"]],
                "check_box": mapping["mpb_enabled"],
            },
        )
    )

    mapping["mbb_enabled"].setToolTip(Hints.MOD_BOSS_BASES)
    mapping["mbb_enabled"].stateChanged.connect(
        lambda: handler(
            "modify/stats/bases/boss",
            {
                "spin_boxes": [parent.spin_boxes["bb_mod"]],
                "check_box": mapping["mbb_enabled"],
            },
        )
    )

    mapping["mob_enabled"].setToolTip(Hints.MOD_OTHER_BASES)
    mapping["mob_enabled"].stateChanged.connect(
        lambda: handler(
            "modify/stats/bases/other",
            {
                "spin_boxes": [parent.spin_boxes["ob_mod"]],
                "check_box": mapping["mob_enabled"],
            },
        )
    )

    mapping["mpg_enabled"].setToolTip(Hints.MOD_PLAYABLE_GROWTHS)
    mapping["mpg_enabled"].stateChanged.connect(
        lambda: handler(
            "modify/stats/growths/playable",
            {
                "spin_boxes": [parent.spin_boxes["pg_mod"]],
                "check_box": mapping["mpg_enabled"],
            },
        )
    )

    mapping["mbg_enabled"].setToolTip(Hints.MOD_BOSS_GROWTHS)
    mapping["mbg_enabled"].stateChanged.connect(
        lambda: handler(
            "modify/stats/growths/boss",
            {
                "spin_boxes": [parent.spin_boxes["bg_mod"]],
                "check_box": mapping["mbg_enabled"],
            },
        )
    )

    mapping["mog_enabled"].setToolTip(Hints.MOD_OTHER_GROWTHS)
    mapping["mog_enabled"].stateChanged.connect(
        lambda: handler(
            "modify/stats/growths/other",
            {
                "spin_boxes": [parent.spin_boxes["og_mod"]],
                "check_box": mapping["mog_enabled"],
            },
        )
    )

    _set_configs(mapping, parent.spin_boxes)

    return mapping
