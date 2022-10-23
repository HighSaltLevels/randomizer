""" Test Suite for FE7 specific item editor """

from unittest import mock

import pytest

from rom_editors.item_editor import ItemNotFoundException
from rom_editors.fe7.item_editor import FE7ItemEditor


# Some tests can only work by using protected attributes and methods.
# pylint: disable=protected-access


@pytest.fixture(name="item_edit")
def create_item_editor(rom_data):
    """ Create an item editor object with FE7 specific items for testing """
    char_edit = FE7ItemEditor(rom_data, mock.MagicMock())
    return char_edit


def test_handle_overrides(item_edit):
    """ Test the handle_overrides method """
    with mock.patch.object(item_edit, "_handle_prf") as m_prf:
        with mock.patch.object(item_edit, "_handle_s_rank") as m_rank:
            item_edit.handle_overrides()
            m_prf.assert_called_once()
            m_rank.assert_called_once()


def test_handle_prf(item_edit):
    """ Test the handle_prf method """
    m_item = mock.MagicMock()
    m_item.weapon = 1
    m_item.equivalent = 2
    item_edit._game_config.items.prfs = [m_item]
    item_edit._game_config.items.first = 0
    item_edit._game_config.sizes.item = 5

    item_edit._handle_prf()

    expected_data = bytearray(byte for byte in range(64))
    expected_data[1] = 0
    assert item_edit.rom_data == expected_data


def test_handle_s_rank(item_edit):
    """ Test the _handle_s_rank method """
    m_weapon = mock.MagicMock()
    m_weapon.rank = "s"
    m_weapon.type = "sword"
    m_weapon.list_ = [20]

    m_char = mock.MagicMock()
    m_char.s_rank_locations = [10]

    item_edit._game_config.items.weapons = [m_weapon]
    item_edit._game_config.char_stats.final_bosses = [mock.MagicMock()]

    with mock.patch.object(item_edit, "_get_item_type") as m_get:
        m_get.return_value = "sword"
        with mock.patch.object(item_edit, "_get_char_by_name") as m_get_char:
            m_get_char.return_value = m_char
            item_edit._handle_s_rank()

    expected_data = bytearray(byte for byte in range(64))
    expected_data[10] = 20
    assert item_edit.rom_data == expected_data


def test_get_char_by_name(item_edit):
    """ Test the _get_char_by_name method """
    m_char = mock.MagicMock()
    m_char.name = "foo"
    item_edit._game_config.characters = [m_char]

    assert item_edit._get_char_by_name("foo") == m_char

    # Test with the character not existing
    with pytest.raises(ValueError) as error:
        item_edit._get_char_by_name("bar")
    assert "No known character bar" in str(error)

def test_get_item_type(item_edit):
    """ Test the _get_item_type method """
    m_weapons = [mock.MagicMock()]
    m_weapons[0].list_ = [69]
    m_weapons[0].type = "foo"
    item_edit._game_config.items.weapons = m_weapons

    assert item_edit._get_item_type(69) == "foo"

    # Test with an item not found
    with pytest.raises(ItemNotFoundException) as error:
        item_edit._get_item_type(420)
    assert "No known item" in str(error)
