""" Test Suite for FE7 specific character edits """

from unittest import mock

import pytest

from rom_editors.fe7.character_editor import FE7CharacterEditor

# Some tests can only work by using protected attributes and methods.
# pylint: disable=protected-access


@pytest.fixture(name="char_edit")
def create_char_editor(rom_data):
    """ Create a character editor """
    char_edit = FE7CharacterEditor(mock.MagicMock(), rom_data, None, False)
    with mock.patch.object(char_edit, "_get_character_by_name") as m_get:
        m_char = mock.MagicMock()
        m_char.id = [0]
        m_char.extra_item_pos = [1]
        m_get.return_value = m_char
        yield char_edit


def test_handle_overrides(char_edit):
    """ Test the handle_overrides method """

    def patch_method(obj, method):
        with mock.patch.object(obj, method):
            pass

    def create_patches(char_edit):
        patches = {
            "_handle_serra_override",
            "_handle_thief_override",
            "_handle_teodor_override",
            "_handle_karla_override",
            "_give_final_bosses_s_ranks",
            "_make_weapons_dropable",
            "_remove_hardcoded_animations",
        }
        for patch in patches:
            patch_method(char_edit, patch)

    create_patches(char_edit)
    char_edit.handle_overrides()


def test_handle_serra_override(char_edit):
    """ Test the _handle_serra_override method """
    char_edit._game_config.char_stats.first = 0
    char_edit._game_config.sizes.character = 5
    char_edit._handle_serra_override()

    expected_data = bytearray(byte for byte in range(64))
    expected_data[17] = 0
    assert char_edit.rom_data == expected_data


def test_handle_thief_override(char_edit):
    """ Test the _handle_thief_override method """
    char_edit._game_config.items.chest_key_id = 50
    char_edit._game_config.items.door_key_id = 51
    char_edit._handle_thief_override()

    expected_data = bytearray(byte for byte in range(64))
    expected_data[1] = 50
    expected_data[2] = 51
    assert char_edit.rom_data == expected_data


def test_handle_teodor_override(char_edit):
    """ Test the _handle_teodor_override method """
    char_edit._game_config.char_stats.overrides.generic_druid_pos = 3
    char_edit._handle_teodor_override()

    expected_data = bytearray(byte for byte in range(64))
    expected_data[3] = 0
    assert char_edit.rom_data == expected_data


def test_handle_karla_override(char_edit):
    """ Test the _handle_karla_override method """
    char_edit._game_config.char_stats.overrides.noops = [4]
    char_edit._handle_karla_override()

    expected_data = bytearray(byte for byte in range(64))
    expected_data[4] = 0
    assert char_edit.rom_data == expected_data


def test_give_final_bosses_s_ranks(char_edit):
    """ Test the _give_final_bosses_s_ranks method """
    m_char = mock.MagicMock()
    m_char.s_rank_locations = [5]
    char_edit._game_config.char_stats.final_bosses = [m_char]
    char_edit._game_config.char_stats.items.first = 20
    char_edit._game_config.sizes.item = 5
    char_edit._game_config.items.offsets.type = 0
    char_edit._game_config.char_stats.first = 0
    char_edit._game_config.sizes.character = 5
    char_edit._game_config.char_stats.offsets.weapon = 4
    char_edit._game_config.items.s_weapon_level = 60
    char_edit._give_final_bosses_s_ranks()

    expected_data = bytearray(byte for byte in range(64))
    expected_data[5] = 1
    assert char_edit.rom_data == expected_data


def test_make_weapons_dropable(char_edit):
    """ Test the _make_weapons_dropable method """
    char_edit._game_config.char_stats.dropable_weapon_characters = [0]
    char_edit._game_config.char_stats.first = 0
    char_edit._game_config.sizes.character = 5
    char_edit._game_config.char_stats.offsets.ability4 = 6
    char_edit._game_config.char_stats.offsets.dropabale_bitmask = 1
    char_edit._make_weapons_dropable()

    expected_data = bytearray(byte for byte in range(64))
    expected_data[6] = 1
    assert char_edit.rom_data == expected_data


def test_remove_hardcoded_animations(char_edit):
    """ Test the remove_hardcoded_animations method """
    m_char = mock.MagicMock()
    m_char.id = [0]
    char_edit._game_config.characters = [m_char]
    char_edit._game_config.char_stats.first = 0
    char_edit._game_config.sizes.character = 5
    char_edit._game_config.char_stats.offsets.animation = 7
    char_edit._remove_hardcoded_animations()

    expected_data = bytearray(byte for byte in range(64))
    expected_data[7] = 0
    expected_data[8] = 0
    assert char_edit.rom_data == expected_data


def test_get_character_by_name(rom_data):
    """ Test the _get_character_by_name method """
    # Use a character editor without the mocked return value
    char_edit = FE7CharacterEditor(mock.MagicMock(), rom_data, None, False)
    m_char = mock.MagicMock()
    m_char.name = "foo"
    char_edit._game_config.characters = [m_char]

    assert isinstance(char_edit._get_character_by_name("foo"), mock.MagicMock)
    with pytest.raises(ValueError) as error:
        char_edit._get_character_by_name("bar")

    assert "No known character named: bar" in str(error)
