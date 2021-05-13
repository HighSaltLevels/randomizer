""" Module for defining all the Labels """

from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

from constants import Hints, NORMAL_FONT, SUBTITLE_FONT, TITLE_FONT


def _add_hints(labels):
    """ Add Tooltip hints to labels """
    labels["randomize"].setToolTip(Hints.RANDOMIZE)
    labels["modify"].setToolTip(Hints.MODIFY)
    labels["playable_bases"].setToolTip(Hints.PLAYABLE_BASES)
    labels["boss_bases"].setToolTip(Hints.BOSS_BASES)
    labels["other_bases"].setToolTip(Hints.OTHER_BASES)
    labels["class_bases"].setToolTip(Hints.CLASS_BASES)
    labels["playable_growths"].setToolTip(Hints.PLAYABLE_GROWTHS)

    labels["mod_playable_bases"].setToolTip(Hints.MOD_PLAYABLE_BASES)
    labels["mod_boss_bases"].setToolTip(Hints.MOD_BOSS_BASES)
    labels["mod_other_bases"].setToolTip(Hints.MOD_OTHER_BASES)
    labels["mod_playable_growths"].setToolTip(Hints.MOD_PLAYABLE_GROWTHS)

    labels["force_master_seal"].setToolTip(Hints.FORCE_MASTER_SEAL)
    labels["class_mode"].setToolTip(Hints.CLASS_MODE)

    for name, label in labels.items():
        if label.text().lower() == "minimum":
            if "_b" in name:
                label.setToolTip(Hints.MIN_BASE_COUNTER)
                continue

            label.setToolTip(Hints.MIN_GROWTH_COUNTER)
            continue

        if label.text().lower() == "maximum":
            if "_b" in name:
                label.setToolTip(Hints.MAX_BASE_COUNTER)
                continue

            label.setToolTip(Hints.MAX_GROWTH_COUNTER)
            continue

        if label.text().lower() == "modifier":
            label.setToolTip(Hints.BASE_MODIFIER)
            continue


def create_labels(widget):
    """ Init and return a dict of all labels """

    # Titles
    randomize = QLabel("Randomize", widget)
    modify = QLabel("Modify", widget)

    # Subtitles
    bases = QLabel("Bases", widget)
    mod_bases = QLabel("Bases", widget)
    etc = QLabel("Etc", widget)
    growths = QLabel("Growths", widget)
    mod_growths = QLabel("Growths", widget)

    labels = {
        "status": QLabel("Status: Initialized", widget),
        "playable_bases": QLabel("Playable", widget),
        "pb_minimum": QLabel("Minimum", widget),
        "pb_maximum": QLabel("Maximum", widget),
        "boss_bases": QLabel("Boss", widget),
        "bb_minimum": QLabel("Minimum", widget),
        "bb_maximum": QLabel("Maximum", widget),
        "other_bases": QLabel("Other", widget),
        "ob_minimum": QLabel("Minimum", widget),
        "ob_maximum": QLabel("Maximum", widget),
        "class_bases": QLabel("Class", widget),
        "cb_minimum": QLabel("Minimum", widget),
        "cb_maximum": QLabel("Maximum", widget),
        "force_master_seal": QLabel("Force Master Seals", widget),
        "playable_growths": QLabel("Playable", widget),
        "pg_minimum": QLabel("Minimum", widget),
        "pg_maximum": QLabel("Maximum", widget),
        "mod_playable_bases": QLabel("Playable", widget),
        "mod_pb": QLabel("Modifier", widget),
        "mod_boss_bases": QLabel("Boss", widget),
        "mod_bb": QLabel("Modifier", widget),
        "mod_other_bases": QLabel("Other", widget),
        "mod_ob": QLabel("Modifier", widget),
        "mod_playable_growths": QLabel("Playable", widget),
        "mod_pg": QLabel("Modifier", widget),
        "class_mode": QLabel("Class Mode", widget),
    }

    for label in labels.values():
        label.setFont(NORMAL_FONT)

    for label in (bases, mod_bases, etc, growths, mod_growths):
        label.setFont(SUBTITLE_FONT)

    for label in (randomize, modify):
        label.setFont(TITLE_FONT)

    labels["randomize"] = randomize
    labels["modify"] = modify

    labels["bases"] = bases
    labels["mod_bases"] = mod_bases
    labels["etc"] = etc
    labels["growths"] = growths
    labels["mod_growths"] = mod_growths

    for label in labels.values():
        label.setAlignment(Qt.AlignCenter)

    labels["status"].setAlignment(Qt.AlignLeft)

    _add_hints(labels)

    return labels
