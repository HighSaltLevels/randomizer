""" Module for defining all the Labels """

from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

from constants import NORMAL_FONT, SUBTITLE_FONT, TITLE_FONT


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
    characters = QLabel("Characters", widget)

    labels = {
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
        "boss_growths": QLabel("Boss", widget),
        "bg_minimum": QLabel("Minimum", widget),
        "bg_maximum": QLabel("Maximum", widget),
        "other_growths": QLabel("Other", widget),
        "og_minimum": QLabel("Minimum", widget),
        "og_maximum": QLabel("Maximum", widget),
        "p_enabled": QLabel("Playable", widget),
        "b_enabled": QLabel("Boss", widget),
        "o_enabled": QLabel("Other", widget),
        "mod_playable_bases": QLabel("Playable", widget),
        "mod_pb": QLabel("Modifier", widget),
        "mod_boss_bases": QLabel("Boss", widget),
        "mod_bb": QLabel("Modifier", widget),
        "mod_other_bases": QLabel("Other", widget),
        "mod_ob": QLabel("Modifier", widget),
        "mod_playable_growths": QLabel("Playable", widget),
        "mod_pg": QLabel("Modifier", widget),
        "mod_boss_growths": QLabel("Boss", widget),
        "mod_bg": QLabel("Modifier", widget),
        "mod_other_growths": QLabel("Other", widget),
        "mod_og": QLabel("Modifier", widget),
    }

    for label in labels.values():
        label.setFont(NORMAL_FONT)

    for label in (bases, mod_bases, etc, growths, mod_growths, characters):
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
    labels["characters"] = characters

    for label in labels.values():
        label.setAlignment(Qt.AlignCenter)

    return labels
