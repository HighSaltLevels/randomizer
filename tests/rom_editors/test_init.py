""" Test Suite for the init functions """

from unittest.mock import MagicMock

from constants import FEVersions
from rom_editors import (
    create_character_editor,
    create_stat_modifier,
    create_stat_randomizer,
    create_prom_editor,
    VERSION_MAP,
)


def test_create_character_editor():
    """ Test the create_character_editor function """
    for version in {FEVersions.FE6, FEVersions.FE7, FEVersions.FE8}:
        char_editor = create_character_editor(
            MagicMock(), MagicMock(), None, None, version
        )
        assert isinstance(char_editor, VERSION_MAP["character"][version])


def test_create_stat_randomizer():
    """ Test the create_stat_randomizer function """
    for version in {FEVersions.FE6, FEVersions.FE7, FEVersions.FE8}:
        stat_rand = create_stat_randomizer(MagicMock(), MagicMock(), version)
        assert isinstance(stat_rand, VERSION_MAP["stat_rand"][version])


def test_create_stat_modifier():
    """ Test the create_stat_modifier function """
    for version in {FEVersions.FE6, FEVersions.FE7, FEVersions.FE8}:
        stat_mod = create_stat_modifier(MagicMock(), MagicMock(), version)
        assert isinstance(stat_mod, VERSION_MAP["stat_mod"][version])


def test_create_prom_editor():
    """ Test the create_stat_randomizer function """
    for version in {FEVersions.FE6, FEVersions.FE7, FEVersions.FE8}:
        prom_edit = create_prom_editor(MagicMock(), MagicMock(), version)
        assert isinstance(prom_edit, VERSION_MAP["prom_edit"][version])
