""" Test Suite for Character Editor """

from unittest import mock

import pytest

from rom_editors.character_editor import CharacterEditor

# Some tests can only work by using protected attributes and methods.
# pylint: disable=protected-access


@pytest.fixture(name="char_editor")
def create_char_editor(game_config, rom_data):
    """ Create a character editor """
    return CharacterEditor(game_config, rom_data, None, False)


@pytest.fixture(name="m_char_editor")
def create_mock_char_editor(rom_data, game_config):
    """ Create a mock character editor with mocked __init__ """
    with mock.patch.object(CharacterEditor, "__init__", lambda a, b, c, d, e: None):
        char_editor = CharacterEditor(None, None, None, False)
        char_editor._game_config = game_config
        char_editor._class_mode = "foo"
        char_editor._mix_promotes = True
        char_editor._class_stats = game_config["classes"]["class_stats"]
        char_editor._rom_data = rom_data
        char_editor._filters = []

        char_editor._item_editor = mock.MagicMock()

        char_editor._get_class_list = mock.MagicMock()
        char_editor._get_class_list.return_value = [200], [300]

        char_editor.get_new_class = mock.MagicMock()
        char_editor.get_new_class.return_value = 100

        char_editor.update_weapon_type = mock.MagicMock()

        char_editor.get_weapon_for_class = mock.MagicMock()
        char_editor.get_weapon_for_class.return_value = 150

        char_editor.randomize_palettes = mock.MagicMock()
        char_editor.add_promotions = mock.MagicMock()
        yield char_editor


def test_set_filters(char_editor):
    """ Test the set_filters method """
    char_editor.set_filters("foo")
    assert char_editor._filters == "foo"


def test_properties(m_char_editor, rom_data):
    """ Test the properties of the CharacterEditor class """
    assert m_char_editor.rom_data == rom_data


def test_get_new_class(char_editor, character_data):
    """ Test the get_new_class method """
    # Test with mix_promotes
    char_editor._mix_promotes = True
    new_class = char_editor.get_new_class([100], [200], character_data["char"])
    # Could be either here
    assert new_class in {100, 200}

    # Test with promotion overrides
    char_editor._mix_promotes = False
    new_class = char_editor.get_new_class([100], [200], character_data["char"])
    # Should always be the promoted class
    assert new_class == 100

    # Test by checking location
    character_data["char"]["id"] = [1]
    new_class = char_editor.get_new_class([1], [2], character_data["char"])
    assert new_class == 2


def test_get_weapon_for_class(char_editor):
    """ Test the get_weapon_for_class_method """
    weapon = char_editor.get_weapon_for_class(2)
    assert weapon == "dark"


def test_get_class_list(char_editor):
    """ Test the _get_class_list method """
    promoted, unpromoted = char_editor._get_class_list()
    assert promoted == []
    assert unpromoted == [0]

    # Change the bitmask to allow all and it should swap promoted and unpromoted
    char_editor._class_stats["promotion"]["bit_mask"] = 7
    promoted, unpromoted = char_editor._get_class_list()
    assert promoted == [0]
    assert unpromoted == []


def test_update_weapon_type(char_editor):
    """ Test the update_weapon_type method """
    with mock.patch.object(char_editor, "_set_weapon_levels_for_class") as m_set:
        char_editor.update_weapon_type(1, [1])
        assert char_editor.rom_data[0] == 1
        m_set.assert_called_once_with(57, 1, 1)
        m_set.reset_mock()

        # Test setting to a weapon level
        char_editor._game_config["classes"]["character_stats"]["weapon_offset"] = 0
        char_editor._rom_data = [0 for _ in range(30)]
        char_editor.update_weapon_type(1, [0])
        assert char_editor.rom_data[0] == 0
        m_set.assert_called_once_with(255, 0, 1)


def test_set_weapon_levels_for_class(char_editor):
    """ Test the _set_weapon_levels_for_class method """
    char_editor._set_weapon_levels_for_class(255, 0, 1)
    assert char_editor.rom_data[0] == 1
    for idx in range(1, 8):
        assert char_editor.rom_data[idx] == 255


def test_randomize_palettes(char_editor):
    """ Test the randomize_palettes method """
    char_editor.randomize_palettes()
    assert char_editor.rom_data[0] == 1
    assert char_editor.rom_data[1] == 49
    assert char_editor.rom_data[2] == 50
    assert char_editor.rom_data[3] == 0
    assert char_editor.rom_data[4] == 0


def test_add_promotions(char_editor):
    """ Test the add_promotions method """
    char_editor.add_promotions()
    assert char_editor.rom_data[0] == 1
    assert char_editor.rom_data[1] == 49
    assert char_editor.rom_data[2] == 50
