""" Module for creating all the spin boxes """
from PyQt5.QtWidgets import QSpinBox

from constants import Hints, NORMAL_FONT
from controller import handler
from config import CONFIG


def _set_config(spin_boxes):
    """Set the states of the spin boxes based on the config"""
    base_configs = CONFIG["randomize"]["stats"]["bases"]
    spin_boxes["pb_min"].setValue(base_configs["playable"]["minimum"])
    spin_boxes["pb_max"].setValue(base_configs["playable"]["maximum"])
    spin_boxes["pb_min"].valueChanged.connect(
        lambda: handler(
            "randomize/stats/bases/playable",
            {"spin_boxes": [spin_boxes["pb_min"], spin_boxes["pb_max"]]},
            toggle=False,
        )
    )
    spin_boxes["pb_max"].valueChanged.connect(
        lambda: handler(
            "randomize/stats/bases/playable",
            {"spin_boxes": [spin_boxes["pb_min"], spin_boxes["pb_max"]]},
            toggle=False,
        )
    )

    spin_boxes["bb_min"].setValue(base_configs["boss"]["minimum"])
    spin_boxes["bb_max"].setValue(base_configs["boss"]["maximum"])
    spin_boxes["bb_min"].valueChanged.connect(
        lambda: handler(
            "randomize/stats/bases/boss",
            {"spin_boxes": [spin_boxes["bb_min"], spin_boxes["bb_max"]]},
            toggle=False,
        )
    )
    spin_boxes["bb_max"].valueChanged.connect(
        lambda: handler(
            "randomize/stats/bases/boss",
            {"spin_boxes": [spin_boxes["bb_min"], spin_boxes["bb_max"]]},
            toggle=False,
        )
    )

    spin_boxes["ob_min"].setValue(base_configs["other"]["minimum"])
    spin_boxes["ob_max"].setValue(base_configs["other"]["maximum"])
    spin_boxes["ob_min"].valueChanged.connect(
        lambda: handler(
            "randomize/stats/bases/other",
            {"spin_boxes": [spin_boxes["ob_min"], spin_boxes["ob_max"]]},
            toggle=False,
        )
    )
    spin_boxes["ob_max"].valueChanged.connect(
        lambda: handler(
            "randomize/stats/bases/other",
            {"spin_boxes": [spin_boxes["ob_min"], spin_boxes["ob_max"]]},
            toggle=False,
        )
    )

    spin_boxes["cb_min"].setValue(base_configs["class"]["minimum"])
    spin_boxes["cb_max"].setValue(base_configs["class"]["maximum"])
    spin_boxes["cb_min"].valueChanged.connect(
        lambda: handler(
            "randomize/stats/bases/class",
            {"spin_boxes": [spin_boxes["cb_min"], spin_boxes["cb_max"]]},
            toggle=False,
        )
    )
    spin_boxes["cb_max"].valueChanged.connect(
        lambda: handler(
            "randomize/stats/bases/class",
            {"spin_boxes": [spin_boxes["cb_min"], spin_boxes["cb_max"]]},
            toggle=False,
        )
    )

    growth_configs = CONFIG["randomize"]["stats"]["growths"]
    spin_boxes["pg_min"].setValue(growth_configs["playable"]["minimum"])
    spin_boxes["pg_max"].setValue(growth_configs["playable"]["maximum"])
    spin_boxes["pg_min"].valueChanged.connect(
        lambda: handler(
            "randomize/stats/growths/playable",
            {"spin_boxes": [spin_boxes["pg_min"], spin_boxes["pg_max"]]},
            toggle=False,
        )
    )
    spin_boxes["pg_max"].valueChanged.connect(
        lambda: handler(
            "randomize/stats/growths/playable",
            {"spin_boxes": [spin_boxes["pg_min"], spin_boxes["pg_max"]]},
            toggle=False,
        )
    )

    mod_configs = CONFIG["modify"]["stats"]
    spin_boxes["pb_mod"].setValue(int(mod_configs["bases"]["playable"]["modifier"]))
    spin_boxes["pb_mod"].valueChanged.connect(
        lambda: handler(
            "modify/stats/bases/playable",
            {"spin_boxes": [spin_boxes["pb_mod"]]},
            toggle=False,
        )
    )

    spin_boxes["bb_mod"].setValue(int(mod_configs["bases"]["boss"]["modifier"]))
    spin_boxes["bb_mod"].valueChanged.connect(
        lambda: handler(
            "modify/stats/bases/boss",
            {"spin_boxes": [spin_boxes["bb_mod"]]},
            toggle=False,
        )
    )

    spin_boxes["ob_mod"].setValue(int(mod_configs["bases"]["other"]["modifier"]))
    spin_boxes["ob_mod"].valueChanged.connect(
        lambda: handler(
            "modify/stats/bases/other",
            {"spin_boxes": [spin_boxes["ob_mod"]]},
            toggle=False,
        )
    )

    spin_boxes["pg_mod"].setValue(int(mod_configs["growths"]["playable"]["modifier"]))
    spin_boxes["pg_mod"].valueChanged.connect(
        lambda: handler(
            "modify/stats/growths/playable",
            {"spin_boxes": [spin_boxes["pg_mod"]]},
            toggle=False,
        )
    )


def create_spin_boxes(widget):
    """Init and return a dict of line edits"""

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
    }
    for name, spin_box in min_max_spin_boxes.items():
        spin_box.setFont(NORMAL_FONT)
        spin_box.setRange(0, 255)
        if "b_max" in name:
            spin_box.setToolTip(Hints.MAX_BASE_COUNTER)
            continue

        if "b_min" in name:
            spin_box.setToolTip(Hints.MIN_BASE_COUNTER)
            continue

        if "g_max" in name:
            spin_box.setToolTip(Hints.MAX_GROWTH_COUNTER)

        if "g_min" in name:
            spin_box.setToolTip(Hints.MIN_GROWTH_COUNTER)

    mod_spin_boxes = {
        "pb_mod": QSpinBox(widget),
        "bb_mod": QSpinBox(widget),
        "ob_mod": QSpinBox(widget),
        "pg_mod": QSpinBox(widget),
    }

    for spin_box in mod_spin_boxes.values():
        spin_box.setFont(NORMAL_FONT)
        spin_box.setRange(-100, 100)
        spin_box.setToolTip(Hints.BASE_MODIFIER)

    spin_boxes = min_max_spin_boxes
    spin_boxes.update(mod_spin_boxes)

    _set_config(spin_boxes)

    return spin_boxes
