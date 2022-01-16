""" conftest.py for building shared fixtures """

from unittest import mock

import pytest


@pytest.fixture(name="m_app")
def create_mock_app():
    """ Patch in a MagicMock() object for QApplication """
    with mock.patch("app.APP") as m_app:
        yield m_app


@pytest.fixture(name="character_data")
def create_character_data():
    """ Create a character_data dict """
    return {"char": {"kind": "playable", "location": [1], "id": [2], "item_pos": [3]}}


@pytest.fixture(name="game_config")
def create_game_config(character_data):
    """ Create a game config option with only values we need """
    return {
        "classes": {
            "class_stats": {
                "first": 0,
                "weapon_offset": 1,
                "bases_offset": 1,
                "total_bytes": 1,
                "num_classes": 4,
                "num_bases": 1,
                "staff_only": [3],
                "blacklist": [1],
                "other": [2],
                "promotion": {"offset": 0, "bit_mask": 0, "overrides": {1: 250}},
                "id_offset": 5,
                "ranged_monster": [6],
            },
            "character_stats": {
                "promotion_overrides": [2],
                "first": 0,
                "total_bytes": 1,
                "weapon_offset": 1,
                "class_offset": 2,
                "bases_offset": 1,
                "growths_offset": 2,
                "num_growths": 1,
                "num_bases": 1,
            },
            "palette_stats": {
                "base_offset": 1,
                "promo_offset": 2,
                "num_palettes": 1,
            },
            "characters": character_data,
        },
        "items": {
            "first": 0,
            "total_bytes": 1,
            "offsets": {
                "type": 9,
                "name": 0,
                "description": 1,
                "use_screen": 2,
                "icon": 3,
                "use": 4,
            },
            "flux_weapon_lvl_pos": 0,
            "a_weapon_lvl": 255,
            "prf": {9: 1},
            "a": {"dark": [69]},
            "ranged_monster": [70],
            "types": {7: "dark"},
            "promotional": {
                "items": {
                    "prom1": {
                        "pointers": [0],
                        "new_location": 1,
                        "item_location": 2,
                    }
                },
                "classes_to_add": [0],
            },
            "master_seal": {
                # Normally there's 2 bytes here, but to avoid race conditions, I'm only using 1
                "name": [0],
                "use_screen": [1],
                "description": [2],
                "icon": 6,
                "use": 7,
            },
        },
    }


@pytest.fixture(name="rom_data")
def create_rom_data():
    """ Create fake rom_data for testing """
    return bytearray(b"0123456789abcdefghijklmnopqrstuvwxyz")
