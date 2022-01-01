""" Test Suite for the StatRandomizer and StatModifier classes """

import copy
from unittest import mock

import pytest

from rom_editors.stat_editor import StatRandomizer, StatModifier, InvalidConfigError


@pytest.fixture(name="stat_rand")
def create_stat_randomizer(game_config, rom_data):
    """ Create a StatRandomizer for testing """
    stat_rand = StatRandomizer(game_config, rom_data)
    stat_rand.set_filters([], [])
    return stat_rand


@pytest.fixture(name="stat_mod")
def create_stat_mod(game_config, rom_data):
    """ Create a StatModifier for testing """
    stat_mod = StatModifier(game_config, rom_data)
    stat_mod.set_filters([], [])
    return stat_mod


def test_randomize(stat_rand):
    """ Test the randomize method """
    with mock.patch.object(stat_rand, "randomize_character_stats") as rand_stat:
        with mock.patch.object(stat_rand, "randomize_class_stats"):
            stat_rand.randomize()
            rand_stat.assert_any_call("bases")
            rand_stat.assert_any_call("growths")


def test_randomize_class_stats(stat_rand):
    """ Test the randomize_class_stats method """
    old_data = copy.deepcopy(stat_rand.rom_data)
    stat_rand.randomize_class_stats()
    # The likelihood that the 4 changed bytes would be the same is low
    # But can happen. If this test fails. Try again ¯\_(ツ)_/¯
    assert stat_rand.rom_data != old_data


def test_randomize_character_stats(stat_rand):
    """ Test the randomize_character_stats method """
    old_data = copy.deepcopy(stat_rand.rom_data)
    for stat_type in {"growths", "bases"}:
        stat_rand.randomize_character_stats(stat_type)
        # The likelihood that the 4 changed bytes would be the same is low
        # But can happen. If this test fails. Try again ¯\_(ツ)_/¯
        assert stat_rand.rom_data != old_data

    # Test the invalid config error due to poor min and max values
    with mock.patch("rom_editors.stat_editor.randint", side_effect=ValueError):
        with pytest.raises(InvalidConfigError):
            stat_rand.randomize_character_stats("bases")


def test_modify(stat_mod):
    """ Test the modify method """
    with mock.patch.object(stat_mod, "modify_character_stats") as mod_stat:
        stat_mod.modify()
        mod_stat.assert_any_call("bases")
        mod_stat.assert_any_call("growths")


def test_modify_character_stats(stat_mod):
    """ Test the modify_character_stats method """
    for stat_type in {"bases", "growths"}:
        stat_mod.modify_character_stats(stat_type)

    assert stat_mod.rom_data[3] == 46
    assert stat_mod.rom_data[4] == 152
