""" Module for holding various constants """

from enum import Enum

from PyQt5.QtGui import QFont

VERSION = "1.0.0"

NORMAL_FONT = QFont()
NORMAL_FONT.setPointSize(10)

SUBTITLE_FONT = QFont()
SUBTITLE_FONT.setPointSize(12)

TITLE_FONT = QFont()
TITLE_FONT.setPointSize(16)

DEFAULT_CONFIG = {
    "randomize": {
        "mix_promotes": {
            "enabled": False,
        },
        "stats": {
            "bases": {
                "playable": {
                    "enabled": False,
                    "minimum": 0,
                    "maximum": 30,
                },
                "boss": {
                    "enabled": False,
                    "minimum": 0,
                    "maximum": 30,
                },
                "other": {
                    "enabled": False,
                    "minimum": 0,
                    "maximum": 30,
                },
                "class": {"enabled": False, "minimum": 0, "maximum": 30},
            },
            "growths": {
                "playable": {"enabled": False, "minimum": 0, "maximum": 255},
                "boss": {"enabled": False, "minimum": 0, "maximum": 255},
                "other": {"enabled": False, "minimum": 0, "maximum": 255},
            },
        },
        "classes": {
            "mode": "Combat",
            "all_master_seals": {
                "enabled": True,
            },
            "playable": {
                "enabled": True,
            },
            "boss": {
                "enabled": True,
            },
            "other": {
                "enabled": True,
            },
        },
    },
    "modify": {
        "stats": {
            "bases": {
                "playable": {"enabled": False, "modifier": -5},
                "boss": {"enabled": False, "modifier": 5},
                "other": {"enabled": False, "modifier": 5},
            },
            "growths": {
                "playable": {"enabled": False, "modifier": -10},
                "boss": {"enabled": False, "modifier": 10},
                "other": {"enabled": False, "modifier": 10},
            },
        }
    },
}


CLASS_MODE_COMBAT = "Combat"
CLASS_MODE_STAFF = "Combat/Staff"
CLASS_MODE_ALL = "All"

CLASS_MODE_OPTIONS = [CLASS_MODE_COMBAT, CLASS_MODE_STAFF, CLASS_MODE_ALL]


class Hints(str, Enum):
    """ ToolTip enumeration class """

    RANDOMIZE = "Configurations for Randomizing character stats and growths"
    MODIFY = "Configurations for modifying character base stats and growths"
    PLAYABLE_BASES = "Enable randomizing of playable character base stats"
    BOSS_BASES = "Enable randomizing of boss character base stats"
    OTHER_BASES = "Enable randomzing of all other npc character base stats"
    CLASS_BASES = "Enable randomizing of base class base stats"

    PLAYABLE_GROWTHS = "Enable randomizing of playable character growth rates"
    BOSS_GROWTHS = "Enable randomizing of boss character growth rates"
    OTHER_GROWTHS = "Enable randomizing of all other npc character growth rates"

    MOD_PLAYABLE_BASES = "Enable modifying of playable character base stats"
    MOD_BOSS_BASES = "Enable modifying of boss character base stats"
    MOD_OTHER_BASES = "Enable modifying of all other npc character base stats"
    MOD_PLAYABLE_GROWTHS = "Enable modifying of playable character growth rates"
    MOD_BOSS_GROWTHS = "Enable modifying of boss character growth rates"
    MOD_OTHER_GROWTHS = "Enable modifying of all other npc character growth rates"

    MAX_BASE_COUNTER = (
        "Set the maximum number that a base stat can reach. "
        "This number cannot excced 255"
    )
    MIN_BASE_COUNTER = (
        "Set the minimum number that a base stat can reach. "
        "This number cannot be less than 0"
    )
    MAX_GROWTH_COUNTER = (
        "Set the maximum number that a growth rate can reach. "
        "This number cannot excced 255"
    )
    MIN_GROWTH_COUNTER = (
        "Set the minimum number that a growth rate can reach. "
        "This number cannot be less than 0"
    )

    BASE_MODIFIER = (
        "Set a modifier to all character base stats (i.e. +5). "
        "This number cannot exceed 100 or be less than -100"
    )

    FORCE_MASTER_SEAL = 'Change all promotion items like "Knight Crest" to Master Seals'

    CLASS_MODE = (
        "Set the mode for randomizing classes.\nCombat - all units guaranteed "
        "to have offensive capabilities\nCombat/Staff - all units are either "
        "offensive or staff only wielders\nAll - Re-roll all classes "
        "(potential soft lock)"
    )

    PLAYABLE_CLASSES = "Randomize all playable character classes"
    BOSS_CLASSES = "Randomize all boss character classes"
    OTHER_CLASSES = "Randomize all other character classes"

    MIX_PROMOTES = (
        "Mix unpromoted unit class with pre-premoted unit classes (Potential Soft Lock)"
    )
