""" Test Suite for FE8 specific character edits """

from unittest import mock

import pytest

from rom_editors.fe8.character_editor import FE8CharacterEditor


# Some tests can only work by using protected attributes and methods.
# pylint: disable=protected-access


@pytest.fixture(name="char_edit")
def create_char_editor(rom_data):
    """Create a character editor with FE8 specific stuff"""
    return FE8CharacterEditor(mock.MagicMock(), rom_data, None, False)


def test_randomize_palettes(char_edit):
    """Test the randomize_palettes method"""
    m_char = mock.MagicMock()
    m_char.id = [10]
    m_char.location = [20]

    char_edit._game_config.characters = [m_char]
    char_edit._game_config.palette_stats.first_palette = 0
    char_edit._game_config.sizes.palette = 2
    char_edit._game_config.totals.palettes = 2
    char_edit._game_config.palette_stats.first_class = 30
    char_edit._game_config.palette_stats.offsets.base_class = 1
    char_edit._game_config.palette_stats.offsets.promoted_class = 8
    char_edit._game_config.sizes.promotion = 5
    char_edit._game_config.totals.promotion_classes = 2

    # With a size of 2, it'll pick either 1 or 0. Let's just make sure
    # The correct addresses are set though.
    char_edit.randomize_palettes()
    assert char_edit.rom_data[20] in {0, 1}
    assert char_edit.rom_data[21] in {0, 1}
