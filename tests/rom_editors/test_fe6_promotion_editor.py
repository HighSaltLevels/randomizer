""" Test Suite for FE6 promotion editors """

from unittest import mock

import pytest

from rom_editors.fe6.promotion_editor import FE6PromotionEditor


# Some tests can only work by using protected attributes and methods.
# pylint: disable=protected-access


@pytest.fixture(name="prom_edit")
def create_prom_editor(rom_data):
    """ Create an FE6PromotionEditor object """
    return FE6PromotionEditor(mock.MagicMock(), rom_data)


def test_handle_overrides(prom_edit):
    """ Test the handle_overrides method """
    m_override = mock.MagicMock()
    m_override.new_location = 5
    m_override.pointer = 6
    m_override.bytes = {7, 8}
    prom_edit._game_config.items.promotional.overrides = [m_override]

    with mock.patch.object(prom_edit, "_parse_pointer") as m_parse:
        m_parse.return_value = {
            10: 69,
            11: 70,
            12: 71,
        }
        prom_edit.handle_overrides()

    expected_data = bytearray(byte for byte in range(64))
    expected_data[5] = 8
    expected_data[6] = 7
    expected_data[7] = 11
    expected_data[8] = 12

    assert prom_edit.rom_data == expected_data
