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
    with mock.patch.object(char_edit, "_handle_f_mercenary_override") as m_merc:
        with mock.patch.object(char_edit, "_handle_cath_override") as m_cath:
            char_edit.handle_overrides()
            m_merc.assert_called_once()
            m_cath.assert_called_once()


def test_handle_f_mercenary_override(char_edit):
    """ Test the handle_f_mercenary_override method """
    m_override = mock.MagicMock()
    m_override.address = 10
    m_override.byte = 69
    char_edit._game_config.char_stats.overrides.f_mercenary = [m_override]

    char_edit._handle_f_mercenary_override()
    expected_data = bytearray(byte for byte in range(64))
    expected_data[10] = 69
    assert char_edit.rom_data == expected_data


def test_handle_cath_override(char_edit):
    """ Test the _handle_cath_override method """
    m_char = mock.MagicMock()
    m_char.extra_item_pos = [0]
    char_edit._game_config.items.chest_key_id = 50
    char_edit._game_config.items.door_key_id = 60

    with mock.patch.object(char_edit, "_get_character_by_name") as m_get:
        m_get.return_value = m_char
        char_edit._handle_cath_override()

    expected_data = bytearray(byte for byte in range(64))
    expected_data[0] = 50
    expected_data[2] = 60
    assert char_edit.rom_data == expected_data
