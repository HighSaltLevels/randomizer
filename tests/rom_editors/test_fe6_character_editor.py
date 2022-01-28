""" Test Suite for FE6 character editors """

from unittest import mock

import pytest

from rom_editors.fe6.character_editor import FE6CharacterEditor


# Some tests can only work by using protected attributes and methods.
# pylint: disable=protected-access


@pytest.fixture(name="char_edit")
def create_char_editor(rom_data):
    """ Create an FE6CharacterEditor object """
    return FE6CharacterEditor(mock.MagicMock(), rom_data, None, False)


def test_handle_overrides(char_edit):
    """ Test the handle_overrides method """
    m_override = mock.MagicMock()
    m_override.address = 10
    m_override.byte = 69
    char_edit._game_config.char_stats.overrides.f_mercenary = [m_override]

    char_edit.handle_overrides()
    expected_data = bytearray(byte for byte in range(64))
    expected_data[10] = 69
    assert char_edit.rom_data == expected_data
