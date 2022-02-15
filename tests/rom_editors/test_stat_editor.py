""" Test Suite for the StatRandomizer and StatModifier classes """

from unittest import mock

import pytest

from rom_editors.stat_editor import (
    StatRandomizer,
    StatModifier,
    InvalidConfigError,
    get_rand,
)
from config import CONFIG


# Some tests can only work by using protected attributes and methods.
# pylint: disable=protected-access


@pytest.fixture(name="stat_rand")
def create_stat_randomizer(rom_data):
    """ Create a StatRandomizer for testing """
    stat_rand = StatRandomizer(mock.MagicMock(), rom_data)
    stat_rand.set_filters([], [])
    return stat_rand


@pytest.fixture(name="stat_mod")
def create_stat_mod(rom_data):
    """ Create a StatModifier for testing """
    stat_mod = StatModifier(mock.MagicMock(), rom_data)
    stat_mod.set_filters([], [])
    return stat_mod


def test_randomize(stat_rand):
    """ Test the randomize method """
    with mock.patch.object(stat_rand, "randomize_character_stats") as m_char:
        with mock.patch.object(stat_rand, "randomize_class_stats") as m_class:
            stat_rand.randomize()
            m_char.assert_called_once()
            m_class.assert_called_once()


def test_randomize_character_stats(stat_rand):
    """ Test the randomize_character_stats method """
    m_char = mock.MagicMock()
    m_char.kind = "boss"
    stat_rand._game_config.characters = [m_char]

    with mock.patch.object(stat_rand, "_randomize_character_stat") as m_rand:
        stat_rand.randomize_character_stats()
        m_rand.assert_called()


def test_randomize_character_stat(stat_rand):
    """ Test the _randomize_character_stat method """
    m_char = mock.MagicMock()
    m_char.id = [0]
    stat_rand._game_config.char_stats.first = 0
    stat_rand._game_config.sizes.character = 5

    with mock.patch("rom_editors.stat_editor.get_rand"):
        stat_rand._randomize_character_stat(m_char, 0, 1, 2, 10)

    expected_values = bytearray(byte for byte in range(64))
    expected_values[10] = 1
    expected_values[11] = 1
    assert stat_rand.rom_data == expected_values


def test_randomize_class_stats(stat_rand):
    """ Test the _randomize_class_stats method """
    stat_rand._game_config.totals.class_ = 1
    stat_rand._game_config.class_stats.first = 0
    stat_rand._game_config.class_stats.offsets.bases = 5
    stat_rand._game_config.class_stats.totals.bases = 2

    with mock.patch("rom_editors.stat_editor.get_rand"):
        stat_rand.randomize_class_stats()

    expected_values = bytearray(byte for byte in range(64))
    expected_values[1] = 1
    assert stat_rand.rom_data == expected_values


def test_modify(stat_mod):
    """ Test the modify method """
    stat_mod._game_config.characters = [mock.MagicMock()]
    with mock.patch.object(stat_mod, "_modify_character_stat") as m_mod:
        stat_mod.modify()
        m_mod.assert_called()


def test_modify_character_stat(stat_mod):
    """ Test the _modify_character_stat method """
    m_char = mock.MagicMock()
    m_char.id = [0]
    m_char.kind = "boss"

    stat_mod._game_config.char_stats.totals.bases = 1
    stat_mod._game_config.char_stats.totals.growths = 1
    stat_mod._game_config.char_stats.offsets.bases = 3
    stat_mod._game_config.char_stats.offsets.growths = 6
    stat_mod._game_config.char_stats.first = 0
    stat_mod._game_config.sizes.character = 10

    # Change the config value to be static. As long as we don't
    # save the config, We're good here.
    CONFIG["modify"]["stats"]["bases"]["boss"]["modifier"] = 20
    CONFIG["modify"]["stats"]["growths"]["boss"]["modifier"] = 20

    stat_mod._modify_character_stat(m_char, "bases")
    stat_mod._modify_character_stat(m_char, "growths")

    # Assert that the values were increased by 20
    expected_values = bytearray(byte for byte in range(64))
    expected_values[3] = 23
    expected_values[6] = 26
    assert stat_mod.rom_data == expected_values


def test_get_rand():
    """ Test the get_rand function """
    # Test with valid configurations
    assert get_rand(0, 50) in range(49)

    # Test with invalid configurations
    with pytest.raises(InvalidConfigError):
        get_rand(0, -50)
