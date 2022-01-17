""" Test Suite for FE7 specific item editor """

from unittest import mock

import pytest

from rom_editors.fe7.item_editor import FE7ItemEditor


@pytest.fixture(name="item_edit")
def create_item_editor(rom_data, game_config):
    """ Create an item editor object with FE7 specific items for testing """
    game_config["items"]["prf"] = {0: 1, 2: 3}
    game_config["items"]["offsets"]["ability3"] = 7
    game_config["items"]["offsets"]["rank"] = 8

    game_config["items"]["flux_weapon_lvl_pos"] = 9
    game_config["items"]["s"] = {"dark": [2]}
    game_config["classes"]["character_stats"]["final_bosses"] = ["boss1"]
    game_config["classes"]["characters"] = {"boss1": {"s_rank_locations": [9]}}
    return FE7ItemEditor(rom_data, game_config)


def test_handle_prf(item_edit):
    """ Test the handle_prf method """
    item_edit.handle_prf()
    assert item_edit.rom_data[7] == 0
    assert item_edit.rom_data[8] == 1
    assert item_edit.rom_data[9] == 0
    assert item_edit.rom_data[10] == 98


def test_handle_s_rank(item_edit):
    """ Test the handle_s_rank method """
    with mock.patch.object(item_edit, "_get_item_type", return_value="dark"):
        item_edit.handle_s_rank()

    assert item_edit.rom_data[9] == 2
