""" Module for generating all line edits """

from pathlib import Path

from PyQt5.QtWidgets import QLineEdit

from config import CONFIG


def create_line_edits(parent):
    """Generate all line edit objects"""
    line_edits = {"rom_edit": QLineEdit(parent)}
    rom_path = CONFIG["rom_path"] if CONFIG.get("rom_path") else str(Path.home())
    line_edits["rom_edit"].setText(rom_path)

    return line_edits
