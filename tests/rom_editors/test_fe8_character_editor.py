""" Test Suite for FE8 specific character edits """

import pytest

from rom_editors.fe8.character_editor import FE8CharacterEditor


@pytest.fixture(name="char_edit")
def create_char_editor(game_config, rom_data):
    """ Create a character editor with FE8 specific stuff """
    game_config["classes"]["promotion_stats"] = {
        "first": 0,
        "total_bytes": 1,
    }
    game_config["classes"]["palette_stats"] = {
        "first_class": 5,
        "first_palette": 10,
        "total_bytes": 1,
        "num_palettes": 1,
        "base_class_offset": 1,
        "promoted_class_offset": 3,
        "num_promoted_classes": 1,
    }
    game_config["classes"]["characters"]["char"]["location"][0] = 0
    return FE8CharacterEditor(game_config, rom_data, None, False)


def test_randomize_palettes(char_edit):
    """ Test the randomize_palettes method """
    char_edit.randomize_palettes()
