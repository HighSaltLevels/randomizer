""" Module for holding various constants """

from PyQt5.QtGui import QFont

NORMAL_FONT = QFont()
NORMAL_FONT.setPointSize(10)

SUBTITLE_FONT = QFont()
SUBTITLE_FONT.setPointSize(12)

TITLE_FONT = QFont()
TITLE_FONT.setPointSize(16)

VERSION = "1.0.0"

DEFAULT_CONFIG = {
    "randomize": {
        "mix_promotes": False,
        "stats": {
            "bases": {
                "playable": {
                    "enabled": False,
                    "range": {"minimum": 0, "maximum": 30},
                    "level": False,
                    "movement": False,
                },
                "other": {
                    "enabled": False,
                    "range": {"minimum": 0, "maximum": 30},
                    "level": False,
                    "movement": False,
                },
                "class": {"enabled": False, "range": {"minimum": 0, "maximum": 30}},
                "max": {
                    "unpromoted": {"enabled": False},
                    "promoted": {"enabled": False},
                },
            },
            "growths": {
                "playable": {"enabled": False, "range": {"minimum": 0, "maximum": 255}},
                "other": {"enabled": False, "range": {"minimum": 0, "maximum": 255}},
            },
            "classes": {"mode": "Combat", "all_master_seals": True},
            "characters": {"playable": True, "bosses": True, "other": True},
        },
    },
    "modify": {
        "stats": {
            "bases": {
                "playable": {"enabled": False, "modifier": -5},
                "other": {"enabled": False, "modifier": 5},
            },
            "growths": {"playable": {"enabled": False, "modifier": -10}},
        }
    },
}
