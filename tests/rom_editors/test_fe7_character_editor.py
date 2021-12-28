""" Test Suite for FE7 specific character edits """

from unittest import mock

import pytest

from rom_editors.fe7.character_editor import FE7CharacterEditor

# Some tests can only work by using protected attributes and methods.
# pylint: disable=protected-access


@pytest.fixture(name="char_editor")
def create_char_editor(game_config, rom_data):
    """ Create a character editor """
    # Add FE7 specific parameters to the game_config here
    game_config["classes"]["class_stats"]["classes"] = {
        "class1": {"promotion_pos": 0, "promotion_id": 15}
    }
    game_config["classes"]["characters"] = {
        "Serra": {"id": [0]},
        "Matthew": {"extra_item_pos": [1]},
        "Teodor": {"id": [150]},
        "boss1": {"s_rank_locations": [1], "id": [6]},
    }
    game_config["classes"]["character_stats"]["overrides"] = {
        "generic_druid_pos": 3,
        "flyers": {4: 200},
    }
    game_config["classes"]["character_stats"]["final_bosses"] = ["boss1"]
    game_config["classes"]["character_stats"]["dropable_weapon_characters"] = [9]
    game_config["classes"]["character_stats"]["offsets"] = {
        "ability4": 9,
        "dropable_bitmask": 16,
    }
    game_config["items"]["chest_key_id"] = 100
    game_config["items"]["door_key_id"] = 101
    game_config["items"]["s_weapon_lvl"] = 255
    return FE7CharacterEditor(game_config, rom_data, None, False)


def test_handle_promotion_targets(char_editor):
    """ Test the handle_promotion_targets method """
    char_editor.handle_promotion_targets()
    assert char_editor.rom_data[0] == 15


def test_handle_serra_override(char_editor):
    """ Test the handle_serra_override method """
    char_editor._handle_serra_override()
    assert char_editor.rom_data[17] == 0


def test_handle_matthew_override(char_editor):
    """ Test the handle_matthew_override method """
    char_editor._handle_matthew_override()
    assert char_editor.rom_data[1] == 100
    assert char_editor.rom_data[2] == 101


def test_handle_teodor_override(char_editor):
    """ Test the handl_ teodor_override_method """
    char_editor._handle_teodor_override()
    assert char_editor.rom_data[3] == 150


def test_handle_flyer_overrides(char_editor):
    """ Test the handle_flyer_overrides method """
    char_editor._handle_flyer_overrides()
    assert char_editor.rom_data[4] == 200


def test_give_final_bosses_s_ranks(char_editor):
    """ Test the give_final_bosses_s_ranks method """
    # Set the weapon ID and type at the calculated index to a low number to
    # avoid Index Out of Bounds issues
    char_editor._rom_data[
        char_editor._game_config["classes"]["characters"]["boss1"]["s_rank_locations"][
            0
        ]
    ] = 5
    char_editor._rom_data[14] = 1
    char_editor._give_final_bosses_s_ranks()
    assert char_editor.rom_data[8] == 255


def test_make_weapons_dropable(char_editor):
    """ Test the make_weapons_dropable method """
    char_editor._make_weapons_dropable()
    assert char_editor.rom_data[18] == 121


def test_handle_overrides(char_editor):
    """ Test all the overrides at once """
    # Mock out the s rank part as it requries a good bit of setup that collides
    # with other overrides
    with mock.patch.object(char_editor, "_give_final_bosses_s_ranks") as m_give:
        char_editor.handle_overrides()
        m_give.assert_called_once()
    assert char_editor.rom_data[17] == 0
    assert char_editor.rom_data[1] == 100
    assert char_editor.rom_data[2] == 101
    assert char_editor.rom_data[3] == 150
    assert char_editor.rom_data[4] == 200
    assert char_editor.rom_data[18] == 121
