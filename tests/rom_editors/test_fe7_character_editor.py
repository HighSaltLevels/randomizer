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
        "Serra": {"id": [0], "kind": "playable"},
        "Matthew": {"id": [0], "extra_item_pos": [1], "kind": "playable"},
        "Legault": {"id": [0], "extra_item_pos": [3], "kind": "playable"},
        "Teodor": {
            "id": [0],
            "kind": "boss",
        },
        "boss1": {"id": [0], "s_rank_locations": [1], "kind": "boss"},
    }
    game_config["classes"]["character_stats"]["overrides"] = {
        "generic_druid_pos": 3,
        "flyers": {4: 200},
        "noops": [21],
    }
    game_config["classes"]["character_stats"]["final_bosses"] = ["boss1"]
    game_config["classes"]["character_stats"]["dropable_weapon_characters"] = [9]
    game_config["classes"]["character_stats"]["offsets"] = {
        "ability4": 9,
        "dropable_bitmask": 16,
        "animation": 19,
    }
    game_config["items"]["chest_key_id"] = 100
    game_config["items"]["door_key_id"] = 101
    game_config["items"]["s_weapon_lvl"] = 255
    return FE7CharacterEditor(game_config, rom_data, None, False)


def test_handle_serra_override(char_editor):
    """ Test the handle_serra_override method """
    char_editor._handle_serra_override()
    assert char_editor.rom_data[17] == 0


def test_handle_thief_override(char_editor):
    """ Test the handle_thief_override method """
    char_editor._handle_thief_override()
    assert char_editor.rom_data[1] == 100
    assert char_editor.rom_data[2] == 101
    assert char_editor.rom_data[3] == 100


def test_handle_teodor_override(char_editor):
    """ Test the handle_teodor_override_method """
    char_editor._handle_teodor_override()
    assert char_editor.rom_data[3] == 0


def test_handle_karla_override(char_editor):
    """ Test the _handle_karla_override method """
    char_editor._handle_karla_override()
    assert char_editor.rom_data[21] == 0


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
    assert char_editor.rom_data[2] == 255


def test_make_weapons_dropable(char_editor):
    """ Test the make_weapons_dropable method """
    char_editor._make_weapons_dropable()
    assert char_editor.rom_data[18] == 121


def test_remove_hardcoded_animations(char_editor):
    """ Test the _remove_hardcoded_animations method """
    char_editor._remove_hardcoded_animations()
    assert char_editor.rom_data[19] == 0
    assert char_editor.rom_data[20] == 0


def test_handle_overrides(char_editor):
    """ Test all the overrides at once """
    # Mock out the s rank part as it requries a good bit of setup that collides
    # with other overrides
    with mock.patch.object(char_editor, "_give_final_bosses_s_ranks") as m_give:
        char_editor.handle_overrides()
        m_give.assert_called_once()
    assert char_editor.rom_data[1] == 100
    assert char_editor.rom_data[2] == 101
    assert char_editor.rom_data[3] == 0
    assert char_editor.rom_data[4] == 52
    assert char_editor.rom_data[17] == 0
    assert char_editor.rom_data[18] == 121
    assert char_editor.rom_data[19] == 0
    assert char_editor.rom_data[20] == 0
    assert char_editor.rom_data[21] == 0
