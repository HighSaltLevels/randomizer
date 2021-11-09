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

        self._handle_serra_override()
        self._handle_matthew_override()

    def _handle_serra_override(self):
        """
        Serra starts with negative resistance because her base class
        has a positive base resistance stat. Since most non-mage classes
        have 0 base res, this commonly causes an int underflow giving her
        max res. Instead, let's initially zero out her res.
        """
        res_offset = 0x11
        serra_ids = self._game_config["classes"]["characters"]["Serra"]["id"]
        first_class = self._game_config["classes"]["character_stats"]["first"]
        total_bytes = self._game_config["classes"]["character_stats"]["total_bytes"]
        for serra_id in serra_ids:
            serra_res_pos = first_class + (serra_id * total_bytes) + res_offset
            self._rom_data[serra_res_pos] = 0

    def _handle_matthew_override(self):
        """
        Although a thief is not required to complete chapter 6, starting Matthew
        with an additional door key and chest key will allow the player to get
        all loot
        """
        extra_item_pos = self._game_config["classes"]["characters"]["Matthew"][
            "extra_item_pos"
        ]
        chest_key_id = self._game_config["items"]["chest_key_id"]
        door_key_id = self._game_config["items"]["door_key_id"]
        self._rom_data[extra_item_pos] = chest_key_id
        self._rom_data[extra_item_pos + 1] = door_key_id
