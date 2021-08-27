""" FE8 Override Class for editing characters """

from random import randint

from rom_editors.character_editor import CharacterEditor
from rom_editors.fe7.item_editor import FE7ItemEditor


class FE7CharacterEditor(CharacterEditor):
    """ FE7 Override to override the ItemEditor """

    def __init__(self, game_config, rom_data, class_mode, mix_promotes):
        super().__init__(game_config, rom_data, class_mode, mix_promotes)
        # Override the item editor
        self._item_editor = FE7ItemEditor(self._rom_data, self._game_config)
