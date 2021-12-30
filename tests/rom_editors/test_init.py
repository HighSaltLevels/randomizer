""" Test Suite for the init functions """

from constants import FEVersions
from rom_editors import (
    create_character_editor,
    create_stat_randomizer,
    create_stat_modifier,
    create_prom_editor,
    VERSION_MAP,
)


def test_create_char_editor(game_config, rom_data):
    """ Test the create_char_editor function """
    for version in {FEVersions.FE6, FEVersions.FE7, FEVersions.FE8}:
        char_editor = create_character_editor(
            game_config, rom_data, None, False, version
        )
        assert isinstance(char_editor, VERSION_MAP["character"][version])


def test_create_stat_randomizer(game_config, rom_data):
    """ Test the create_stat_randomizer function """
    for version in {FEVersions.FE6, FEVersions.FE7, FEVersions.FE8}:
        stat_rand = create_stat_randomizer(game_config, rom_data, version)
        assert isinstance(stat_rand, VERSION_MAP["stat_rand"][version])


def test_create_stat_modifier(game_config, rom_data):
    """ Test the create_stat_modifier function """
    for version in {FEVersions.FE6, FEVersions.FE7, FEVersions.FE8}:
        stat_mod = create_stat_modifier(game_config, rom_data, version)
        assert isinstance(stat_mod, VERSION_MAP["stat_mod"][version])


def test_create_prom_editor(game_config, rom_data):
    """ Test the create_stat_randomizer function """
    for version in {FEVersions.FE6, FEVersions.FE7, FEVersions.FE8}:
        prom_edit = create_prom_editor(game_config, rom_data, version)
        assert isinstance(prom_edit, VERSION_MAP["prom_edit"][version])
