""" Test Suite for Item Editor """

from unittest import mock

import pytest

from rom_editors.item_editor import ItemEditor, ItemException, ItemNotFoundException

# Some tests can only work by using protected attributes and methods.
# pylint: disable=protected-access


@pytest.fixture(name="item_edit")
def create_item_editor(rom_data):
    """ Create an ItemEditor for testing """
    return ItemEditor(rom_data, mock.MagicMock())


@pytest.fixture(name="m_weapons")
def create_mock_weapons():
    """ Create a list of a single MagicMock() object """
    m_weapon = mock.MagicMock()
    m_weapon.type = "sword"
    m_weapon.rank = "a"
    m_weapon.list_ = [100]
    return [m_weapon]


def test_randomize(item_edit):
    """ Test the randomize method """
    item_edit._item_pos = [69]

    with mock.patch.object(item_edit, "randomize_item") as m_rand:
        item_edit.randomize()
        m_rand.assert_called_once()


def test_randomize_item(item_edit):
    """ Test the randomize_item method """
    # Set up parameters
    m_prf = mock.MagicMock()
    m_prf.weapon = 20
    m_prf.equivalent = 21
    item_edit._game_config.items.prfs = [m_prf]

    # Test the manaketes get their respective stones
    item_edit._new_class = 69
    item_edit._game_config.class_stats.manakete = 69
    item_edit._game_config.items.dragonstone = 50
    item_edit.randomize_item(1)
    assert item_edit.rom_data[1] == 50
    item_edit._game_config.class_stats.manakete = 255

    item_edit._game_config.class_stats.manakete_f = 69
    item_edit._game_config.items.divinestone = 51
    item_edit.randomize_item(2)
    assert item_edit.rom_data[2] == 51
    item_edit._game_config.class_stats.manakete_f = 255

    with mock.patch.object(item_edit, "_get_item_type"):
        with mock.patch.object(item_edit, "_get_item_rank"):
            with mock.patch.object(item_edit, "_create_weapon_list") as m_weapon:
                m_weapon.return_value = [70]

                # Test iron sowrd. We can use the 0th position as it will
                # indicate an iron sword that way
                item_edit.randomize_item(0)
                assert item_edit.rom_data[0] == 70

                # Test prf item replacement
                item_edit.randomize_item(20)
                assert item_edit.rom_data[20] == 70

                # Test removal of ranged_monster_items
                item_edit._class_pos = 30
                item_edit._game_config.class_stats.offsets.id = 0
                item_edit._game_config.items.ranged_monster = [60]
                m_weapon.return_value = [60, 70]
                # 60 should get filtered out and just leave 70 so there
                # should be no randomization issues here
                item_edit.randomize_item(40)
                assert item_edit.rom_data[40] == 70


def test_load(item_edit):
    """ Test the load method """
    item_edit._game_config._class_stats.first = 0
    item_edit._game_config.sizes.class_ = 6
    item_edit.load(10, 11, "sword")
    assert item_edit._item_pos == 10
    assert item_edit._weapon_type == "sword"
    assert item_edit._new_class == 11


def test_get_item_rank(item_edit, m_weapons):
    """ Test the _get_item_rank method """
    item_edit._game_config.items.weapons = m_weapons

    # Test with the item found
    assert item_edit._get_item_rank("sword") == m_weapons[0].rank

    # Test with an item not found
    with pytest.raises(ItemException) as error:
        item_edit._get_item_rank(69)

    assert "Could not determine rank of item" in str(error)


def test_get_item_type(item_edit, m_weapons):
    """ Test the _get_item_type method """
    item_edit._game_config.items.weapons = m_weapons

    # Test with an item found
    assert item_edit._get_item_type(100) == m_weapons[0].type

    # Test with an item not found
    with pytest.raises(ItemNotFoundException) as error:
        item_edit._get_item_type(69)

    assert "No known item" in str(error)


def test_create_weapon_list(item_edit, m_weapons):
    """ Test the _create_weapon_list method """
    item_edit._game_config.items.weapons = m_weapons

    # Test with the item found
    assert item_edit._create_weapon_list("a", "sword") == m_weapons[0].list_

    # Test with an item not found
    with pytest.raises(ItemException) as error:
        item_edit._create_weapon_list("b", "foo")

    assert "Could not find suitable match for rank" in str(error)
