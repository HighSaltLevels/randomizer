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

    def handle_promotion_targets(self):
        """
        Make a few exceptions for certain classes to allow more variety
          - Allow female theives to class change. Not sure why this isn't default
          - Make Knight Lord the target promotion class of soldiers
        """
        classes = self._game_config["classes"]["class_stats"]["classes"]
        for _class in classes:
            self._rom_data[classes[_class]["promotion_pos"]] = classes[_class][
                "promotion_id"
            ]

    def handle_overrides(self):
        """ Set the matthew and serra overrides """
        self._handle_serra_override()
        self._handle_matthew_override()
        self._give_final_bosses_s_ranks()

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
        chest_key_id = self._game_config["items"]["chest_key_id"]
        door_key_id = self._game_config["items"]["door_key_id"]
        for item_pos in self._game_config["classes"]["characters"]["Matthew"][
            "extra_item_pos"
        ]:
            self._rom_data[item_pos] = chest_key_id
            self._rom_data[item_pos + 1] = door_key_id

    def _give_final_bosses_s_ranks(self):
        """
        Now that final bosses have s rank weapons, we need to go in and give them
        the proper weapon lvls for those s ranks
        """
        character_stats = self._game_config["classes"]["character_stats"]
        for boss in character_stats["final_bosses"]:
            weapon_id = self._rom_data[
                self._game_config["classes"]["characters"][boss]["s_rank_locations"][0]
            ]

            first = self._game_config["items"]["first"]
            total_bytes = self._game_config["items"]["total_bytes"]
            type_offset = self._game_config["items"]["offsets"]["type"]
            weapon_type = self._rom_data[
                first + (weapon_id * total_bytes) + type_offset
            ]

            for char_id in self._game_config["classes"]["characters"][boss]["id"]:
                first = character_stats["first"]
                total_bytes = character_stats["total_bytes"]
                weapon_offset = character_stats["weapon_offset"]
                self._rom_data[
                    first + (char_id * total_bytes) + weapon_offset + weapon_type
                ] = self._game_config["items"]["s_weapon_lvl"]
