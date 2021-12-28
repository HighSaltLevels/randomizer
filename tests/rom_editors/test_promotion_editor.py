""" Test Suite for Promotion Editor """

from unittest import mock

import pytest

from rom_editors.promotion_editor import PromotionEditor, parse_pointer

# Some tests can only work by using protected attributes and methods.
# pylint: disable=protected-access


@pytest.fixture(name="prom_edit")
def create_prom_edit(game_config, rom_data):
    """ Create a PromotionEditor for testing """
    return PromotionEditor(game_config, rom_data)


@mock.patch("rom_editors.promotion_editor.PromotionEditor._do_single_byte_categories")
@mock.patch("rom_editors.promotion_editor.PromotionEditor._do_multi_bytes_categories")
def test_make_all_master_seals(m_single, m_multi, prom_edit):
    """ Test the make_all_master_seals method """
    prom_edit.make_all_master_seals()
    m_single.assert_called_once_with(prom_edit._game_config["items"]["offsets"], 2)
    m_multi.assert_called_once_with(prom_edit._game_config["items"]["offsets"], 2)


def test_add_classes_to_promotion(prom_edit):
    """ Test the add_classes_to_promotion method """
    with mock.patch(
        "rom_editors.promotion_editor.parse_pointer", return_value=(1, 2, 3)
    ):
        prom_edit.add_classes_to_promotion()

    assert prom_edit.rom_data[0] == 1
    assert prom_edit.rom_data[1] == 0
    assert prom_edit.rom_data[2] == 0


def test_do_single_byte_categories(prom_edit):
    """ Test the _do_single_byte_categories method """
    offsets = prom_edit._game_config["items"]["offsets"]
    prom_edit._do_single_byte_categories(offsets, 5)
    assert prom_edit.rom_data[8] == 6
    assert prom_edit.rom_data[9] == 7


def test_do_multi_bytes_categories(prom_edit):
    """ Test the _do_multi_bytes_categories method """
    offsets = prom_edit._game_config["items"]["offsets"]
    prom_edit._do_multi_bytes_categories(offsets, 5)
    assert prom_edit.rom_data[5] == 0
    assert prom_edit.rom_data[6] == 2
    assert prom_edit.rom_data[7] == 1


def test_parse_pointer():
    """ Test the parse_pointer function """
    byte1, byte2, byte3 = parse_pointer(0x123456)
    assert byte1 == 86
    assert byte2 == 52
    assert byte3 == 18
