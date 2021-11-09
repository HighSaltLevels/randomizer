""" Import everything from this directory """

from versions import FEVersions
from .fe7.character_editor import *
from .fe8.character_editor import *

from .character_editor import CharacterEditor
from .stat_editor import StatRandomizer, StatModifier
from .promotion_editor import PromotionEditor

# FE6 and FE7 are close enough that they can share editors.
# FE8 changed a lot with the new promotion system
VERSION_MAP = {
    "character": {
        FEVersions.FE6: CharacterEditor,
        FEVersions.FE7: FE7CharacterEditor,
        FEVersions.FE8: FE8CharacterEditor,
    },
    "stat_rand": {
        FEVersions.FE6: StatRandomizer,
        FEVersions.FE7: StatRandomizer,
        FEVersions.FE8: StatRandomizer,
    },
    "stat_mod": {
        FEVersions.FE6: StatModifier,
        FEVersions.FE7: StatModifier,
        FEVersions.FE8: StatModifier,
    },
    "prom_edit": {
        FEVersions.FE6: PromotionEditor,
        FEVersions.FE7: PromotionEditor,
        FEVersions.FE8: PromotionEditor,
    },
}


def create_character_editor(
    game_config, rom_data, class_mode, mix_promotes, fe_version
):
    """ Return a CharacterEditor based on FE version """
    return VERSION_MAP["character"][fe_version](
        game_config, rom_data, class_mode, mix_promotes
    )


def create_stat_randomizer(game_config, rom_data, fe_version):
    """ Return a StatRandomizer based on FE version """
    return VERSION_MAP["stat_rand"][fe_version](game_config, rom_data)


def create_stat_modifier(game_config, rom_data, fe_version):
    """ Return a StatModifier based on FE version """
    return VERSION_MAP["stat_mod"][fe_version](game_config, rom_data)


def create_prom_editor(game_config, rom_data, fe_version):
    """ Return a PromotionEditor base on FE version """
    return VERSION_MAP["prom_edit"][fe_version](game_config, rom_data)
