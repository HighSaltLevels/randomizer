""" Test Suite for Character Editor """

from unittest import mock

import pytest

from rom_editors.character_editor import CharacterEditor

# Some tests can only work by using protected attributes and methods.
# pylint: disable=protected-access


@pytest.fixture(name="char_editor")
def create_char_editor(rom_data):
    """ Create a character editor """
    # Always force randint to pick the first entry
    with mock.patch("rom_editors.character_editor.randint") as m_rand:
        m_rand.return_value = 0
        yield CharacterEditor(mock.MagicMock(), rom_data, None, False)


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
    test_filter = ["1", "2", "3"]
    char_editor.set_filters(test_filter)
    assert char_editor._filters == test_filter


def test_randomize(char_editor):
    """ Test the randomize method """
    m_char = mock.MagicMock()
    m_char.kind = "foo"
    m_char.location = [8]
    m_char.item_pos = 16
    char_editor._game_config.characters = [m_char]
    char_editor._item_editor = mock.MagicMock()

    with mock.patch.object(char_editor, "randomize_palettes"):
        with mock.patch.object(char_editor, "add_promotions"):
            with mock.patch.object(char_editor, "fix_flyers"):
                with mock.patch.object(char_editor, "get_new_class"):
                    expected_values = bytearray(byte for byte in range(64))
                    expected_values[8] = 1
                    assert char_editor.randomize() == expected_values


def test_get_new_class(char_editor):
    """ Test the get_new_class method """
    promoted = [1]
    unpromoted = [2]
    both = promoted + unpromoted
    char_editor._game_config.char_stats.promotion_overrides = [3]

    # Test with self._mix_promotes set to True
    char_editor._mix_promotes = True
    assert char_editor.get_new_class(promoted, unpromoted, None) == both[0]

    # Test with promotion overrides
    char_editor._mix_promotes = False
    m_char = mock.MagicMock()
    m_char.id = [3]
    assert char_editor.get_new_class(promoted, unpromoted, m_char) == promoted[0]
    m_char.id = [4]  # Reset to a value that doesn't indicate promotion override

    # Test with character in promoted
    with mock.patch.object(
        char_editor, "_get_current_class", mock.MagicMock()
    ) as m_get:
        m_get.return_value = promoted[0]
        assert char_editor.get_new_class(promoted, unpromoted, m_char) == promoted[0]

    # Test with character in unpromoted
    with mock.patch.object(
        char_editor, "_get_current_class", mock.MagicMock()
    ) as m_get:
        m_get.return_vlue = unpromoted[0]
        assert char_editor.get_new_class(promoted, unpromoted, m_char) == unpromoted[0]


def test_get_weapon_type_for_class(char_editor):
    """ Test the get_weapon_type_for_class method """
    char_editor._game_config.class_stats.staff_only = [3]

    char_editor._game_config.class_stats.first = 0
    char_editor._game_config.class_stats.offsets.weapon = 1
    char_editor._game_config.sizes.class_ = 1
    assert char_editor.get_weapon_type_for_class(1) == "dark"


def test_get_current_class(char_editor):
    """ Test the _get_current_class method """
    char_editor._game_config.char_stats.first = 0
    char_editor._game_config.char_stats.offsets.class_ = 1
    char_editor._game_config.sizes.character = 1

    assert char_editor._get_current_class(5) == 6


def test_get_class_list(char_editor):
    """ Test the _get_class_list method """
    char_editor._game_config.class_stats.first = 0
    char_editor._game_config.sizes.class_ = 3
    char_editor._game_config.totals.class_ = 10

    char_editor._game_config.class_stats.blacklist = [1]
    char_editor._game_config.class_stats.other = [2]
    char_editor._game_config.class_stats.staff_only = [3]

    char_editor._game_config.class_stats.offsets.promotion = 1
    char_editor._game_config.class_stats.promotion.bit_mask = 1

    promoted, unpromoted = char_editor._get_class_list()
    assert promoted == [0, 4, 6, 8]
    assert unpromoted == [5, 7, 9]


def test_update_weapon_type(char_editor):
    """ Test the update_weapon_type method """
    char_editor._game_config.char_stats.first = 0
    char_editor._game_config.sizes.character = 3
    char_editor._game_config._char_stats.offsets.weapon = 1
    char_editor._game_config.items.a_weapon_lvl = 255

    with mock.patch.object(char_editor, "_set_weapon_levels_for_class") as m_set:
        char_editor.update_weapon_type(new_class=69, ids=[0, 1, 2])
        m_set.assert_called_with(255, 6, 69)


def test_set_weapon_levels_for_class(char_editor):
    """ Test the _set_weapon_levels_for_class method """
    char_editor._game_config.class_stats.first = 0
    char_editor._game_config.sizes.class_ = 3
    char_editor._game_config.class_stats.offsets.weapon = 1

    char_editor._set_weapon_levels_for_class(69, 3, 10)

    expected_values = bytearray(byte for byte in range(64))
    expected_values[1] = 69
    assert char_editor.rom_data == expected_values


def test_randomize_palettes(char_editor):
    """ Test the randomize_palettes method """
    m_char = mock.MagicMock()
    m_char.id = [1, 2]
    char_editor._game_config.characters = [m_char]
    char_editor.set_filters([])

    char_editor._game_config.palette_stats.offsets.base = 1
    char_editor._game_config.palette_stats.offsets.promo = 2
    char_editor._game_config.totals.palettes = 2
    char_editor._game_config.char_stats.first = 0
    char_editor._game_config.sizes.character = 10

    char_editor.randomize_palettes()

    expected_values = bytearray(byte for byte in range(64))
    for expected_zero in {11, 12, 21, 22}:
        expected_values[expected_zero] = 0

    assert char_editor.rom_data == expected_values


def test_add_promotions(char_editor):
    """ Test the add_promotions_method """
    m_override = mock.MagicMock()
    m_override.unprom_class = 3
    m_override.prom_class = 6
    char_editor._game_config.class_stats.promotion.overrides = [m_override]
    char_editor._game_config.class_stats.first = 0
    char_editor._game_config.sizes.class_ = 10
    char_editor._game_config.char_stats.offsets.class_ = 2

    char_editor.add_promotions()

    expected_values = bytearray(byte for byte in range(64))
    expected_values[32] = 6
    assert char_editor.rom_data == expected_values


def test_fix_flyers(char_editor):
    """ Test the fix_flyers method """
    m_override = mock.MagicMock()
    m_override.address = 5
    m_override.byte = 255
    char_editor._game_config.char_stats.overrides.flyers = [m_override]

    char_editor.fix_flyers()
    expected_values = bytearray(byte for byte in range(64))
    expected_values[5] = 255
    assert char_editor.rom_data == expected_values
