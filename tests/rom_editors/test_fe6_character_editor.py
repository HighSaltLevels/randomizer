""" Test Suite for FE6 character editors """

from unittest import mock

import pytest

from rom_editors.fe6.character_editor import FE6CharacterEditor


# Some tests can only work by using protected attributes and methods.
# pylint: disable=protected-access


@pytest.fixture(name="char_edit")
def create_char_editor(rom_data):
    """Create an FE6CharacterEditor object"""
    return FE6CharacterEditor(mock.MagicMock(), rom_data, None, False)


def test_handle_overrides(char_edit):
    """Test the handle_overrides method"""
    with mock.patch.object(char_edit, "_handle_f_mercenary_override") as m_merc:
        with mock.patch.object(char_edit, "_handle_chad_override") as m_chad:
            with mock.patch.object(char_edit, "_handle_cath_override") as m_cath:
                with mock.patch.object(char_edit, "_handle_roy_override") as m_roy:
                    char_edit.handle_overrides()
                    m_merc.assert_called_once()
                    m_chad.assert_called_once()
                    m_cath.assert_called_once()
                    m_roy.assert_called_once()


def test_handle_f_mercenary_override(char_edit):
    """Test the handle_f_mercenary_override method"""
    m_override = mock.MagicMock()
    m_override.address = 10
    m_override.byte = 69
    char_edit._game_config.char_stats.overrides.f_mercenary = [m_override]

    char_edit._handle_f_mercenary_override()
    expected_data = bytearray(byte for byte in range(64))
    expected_data[10] = 69
    assert char_edit.rom_data == expected_data


def test_handle_chad_override(char_edit):
    """Test the handle_chad_override method"""
    m_char = mock.MagicMock()
    m_char.extra_item_pos = [16]

    with mock.patch.object(char_edit, "_get_character_by_name") as m_get:
        m_get.return_value = m_char
        char_edit._handle_chad_override()

    expected_data = bytearray(byte for byte in range(64))
    expected_data[16] = 1
    expected_data[17] = 1
    assert char_edit.rom_data == expected_data


def test_handle_cath_override(char_edit):
    """Test the _handle_cath_override method"""
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


def test_handle_roy_override():
    """Test the _handle_roy_override method"""
    # So much data is changed with the Roy override that it's better
    # to just create our own Editor and rom_data
    rom_data = bytearray(byte for byte in range(64))
    char_edit = FE6CharacterEditor(mock.MagicMock(), rom_data, None, False)

    m_char = mock.MagicMock()
    m_char.location = [5]
    m_char.story_prom_locations = [10]
    char_edit._game_config.class_stats.first = 0
    char_edit._game_config.class_stats.offsets.ability2 = 30
    char_edit._game_config.sizes.class_ = 5
    char_edit._game_config.class_stats.bit_masks.lord = 0x1

    with mock.patch.object(char_edit, "_get_character_by_name") as m_get:
        m_get.return_value = m_char
        char_edit._handle_roy_override()

    # The resulting bytearray should have at 32 bytes changed due to
    # skipping Roy's promotion subroutine. Since the method we're testing
    # is using test data that is incrementing at every byte, we can set up
    # the expected values the same way.
    expected_data = bytearray(byte for byte in range(64))
    expected_data[1] = 0
    for i in range(32):
        expected_data[10 + i] = 26 + i

    # Roy's promotion class should also have the toggled "lord" bit
    expected_data[14] |= char_edit._game_config.class_stats.bit_masks.lord

    assert char_edit.rom_data == expected_data
