""" Test Suite for Item Editor """

from unittest import mock

import pytest

from rom_editors.item_editor import ItemEditor, ItemException, ItemNotFoundException

# Some tests can only work by using protected attributes and methods.
# pylint: disable=protected-access


@pytest.fixture(name="item_edit")
def create_item_editor(rom_data, game_config):
    """ Create an ItemEditor for testing """
    return ItemEditor(rom_data, game_config)


@pytest.fixture(name="m_item_edit")
def create_mock_item_editor(rom_data, game_config):
    """ Create a mock ItemEditor for testing """
    game_config["classes"]["class_stats"]["manakete"] = 1000
    game_config["items"]["dragonstone"] = 99
    game_config["items"]["ranged_monster"] = [101]
    with mock.patch.object(ItemEditor, "_get_item_type", return_value="dark"):
        with mock.patch.object(ItemEditor, "_get_item_lvl", return_value="a"):
            yield ItemEditor(rom_data, game_config)


def test_randomize(item_edit):
    """ Test the randomize method """
    item_edit.load([3], 1, "dark")
    with mock.patch.object(item_edit, "randomize_item") as m_rand:
        item_edit.randomize()
        m_rand.assert_called_once_with(3)


def test_randomize_item_manakete(m_item_edit):
    """ Test with manakete as the new class """
    m_item_edit.load([3], 1000, "dark")
    m_item_edit.randomize_item(10)
    assert m_item_edit.rom_data[10] == 99


def test_randomize_item_iron_weapon(m_item_edit):
    """ Test where we want to assign iron weapon """
    m_item_edit.load([3], 1, "dark")
    m_item_edit._rom_data[0] = 0
    m_item_edit.randomize_item(0)
    assert m_item_edit.rom_data[0] == 69


def test_randomize_item_prf(m_item_edit):
    """ Test where we end up with a prf item to replace """
    m_item_edit.load([3], 1, "dark")
    m_item_edit._rom_data[0] = 9
    m_item_edit.randomize_item(0)
    assert m_item_edit.rom_data[0] == 69


def test_randomize_ranged_monster(m_item_edit):
    """ Test where the item can only be used for ranged_monsters """
    m_item_edit.load([3], 1, "dark")
    m_item_edit._rom_data[0] = 101
    m_item_edit._game_config["items"]["a"]["dark"] = [69, 101]
    m_item_edit.randomize_item(0)
    assert m_item_edit.rom_data[0] == 69


def test_get_item_lvl(item_edit):
    """ Test the _get_item_lvl method """
    item_lvl_map = {"e": 0, "d": 1, "c": 2, "b": 3, "a": 4, "s": 5}
    for lvl, idx in item_lvl_map.items():
        item_edit._game_config["items"][lvl] = {"dark": [idx]}

    for lvl, idx in item_lvl_map.items():
        level = item_edit._get_item_lvl(idx, "dark")
        assert level == lvl

    # Test with indeterminate item
    with pytest.raises(ItemException) as error:
        item_edit._get_item_lvl(69, "dark")
        assert "Could not determine level" in str(error)


def test_get_item_type(item_edit):
    """ Test the _get_item_type method """
    with mock.patch.object(item_edit, "_get_items", return_value=[30]):
        _type = item_edit._get_item_type(30)
        assert _type == "dark"

    # Make sure you can catch the generic Item Exception too
    with mock.patch.object(item_edit, "_get_items", return_value=[30]):
        for exception in {ItemException, ItemNotFoundException}:
            with pytest.raises(exception) as error:
                item_edit._get_item_type(0)
                assert "No known item 0" in str(error)


def test_get_items(item_edit):
    """ Test the _get_items method """
    item_edit._game_config["items"] = {
        "e": {"dark": [0]},
        "d": {"dark": [1]},
        "c": {"dark": [2]},
        "b": {"dark": [3]},
        "a": {"dark": [4]},
        "s": {"dark": [5]},
    }
    items = item_edit._get_items("dark")
    for idx in range(6):
        assert idx in items
