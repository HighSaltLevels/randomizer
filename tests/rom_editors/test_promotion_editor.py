""" Test Suite for Promotion Editor """

from unittest import mock

import pytest

from rom_editors.promotion_editor import PromotionEditor

# Some tests can only work by using protected attributes and methods.
# pylint: disable=protected-access


@pytest.fixture(name="prom_edit")
def create_prom_edit(rom_data):
    """ Create a PromotionEditor for testing """
    return PromotionEditor(mock.MagicMock(), rom_data)


def test_make_all_master_seals(prom_edit):
    """ Test the make_all_master_seals method """
    prom_edit._game_config.items.promotional.items = [mock.MagicMock()]
    with mock.patch.object(prom_edit, "_setup_prom_item") as m_setup:
        with mock.patch.object(prom_edit, "_add_classes_to_promotion") as m_add:
            prom_edit.make_all_master_seals()
            m_setup.assert_called_once()
            m_add.assert_called_once()


def test_add_classes_to_promotion(prom_edit):
    """ Test the _add_classes_to_promotion method """
    m_item = mock.MagicMock()
    m_item.pointers = [10]
    m_item.new_location = 20
    prom_edit._game_config.items.promotional.classes_to_add = [30]

    with mock.patch.object(prom_edit, "_parse_pointer") as m_parse:
        m_parse.return_value = 1, 2, 3
        prom_edit._add_classes_to_promotion(m_item)

    expected_values = bytearray(byte for byte in range(64))
    expected_values[10] = 1
    expected_values[11] = 2
    expected_values[12] = 3
    expected_values[20] = 30
    expected_values[21] = 0
    assert prom_edit.rom_data == expected_values


def test_setup_prom_item(prom_edit):
    """ Test the _setup_prom_item method """
    m_attr = mock.MagicMock()
    m_attr.bytes = [200, 201]
    m_attr.offset = 0
    prom_edit._game_config.items.master_seal.attributes = [m_attr]

    prom_edit._setup_prom_item(5)
    expected_values = bytearray(byte for byte in range(64))
    expected_values[5] = 200
    expected_values[6] = 201
    assert prom_edit.rom_data == expected_values


def test_parse_pointer(prom_edit):
    """ Test the parse_pointer method """
    assert prom_edit._parse_pointer(0x123456) == (0x56, 0x34, 0x12)
