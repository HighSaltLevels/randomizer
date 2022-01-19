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
