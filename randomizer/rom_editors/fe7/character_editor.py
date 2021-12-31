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
        self._handle_flyer_overrides()
        self._handle_teodor_override()
        self._give_final_bosses_s_ranks()
        self._make_weapons_dropable()
        self._remove_hardcoded_animations()

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

    def _handle_teodor_override(self):
        """
        Replace the generic Druid that's holding Gespenst with the character
        Teodor.
        """
        teodor_id = self._game_config["classes"]["characters"]["Teodor"]["id"][0]
        generic_druid_pos = self._game_config["classes"]["character_stats"][
            "overrides"
        ]["generic_druid_pos"]
        self._rom_data[generic_druid_pos] = teodor_id

    def _handle_flyer_overrides(self):
        """
        When certain units who were flying get randomized into ground units, it can
        break the game if the cutscene calls for flying over mountains or water. These
        tweaks start the unit into terrain tiles that will allow safe navigation to
        their destination.
        """
        for address, byte in self._game_config["classes"]["character_stats"][
            "overrides"
        ]["flyers"].items():
            self._rom_data[address] = byte

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

    def _make_weapons_dropable(self):
        """
        Make Nergal's, Morph Linus's, and Morph Jerme's weapons dropable.
        It's done through changing a bit on ability 4 on the character.
        """
        character_stats = self._game_config["classes"]["character_stats"]
        for _id in character_stats["dropable_weapon_characters"]:
            first = character_stats["first"]
            offset = (character_stats["total_bytes"] * _id) + character_stats[
                "offsets"
            ]["ability4"]
            self._rom_data[first + offset] = (
                self._rom_data[first + offset]
                | character_stats["offsets"]["dropable_bitmask"]
            )

    def _remove_hardcoded_animations(self):
        """
        Some characters are given hardcoded animations. Let's remove them
        """
        characters = self._game_config["classes"]["characters"]
        first = self._game_config["classes"]["character_stats"]["first"]
        total_bytes = self._game_config["classes"]["character_stats"]["total_bytes"]
        offset = self._game_config["classes"]["character_stats"]["offsets"]["animation"]
        for character in characters:
            if characters[character]["kind"] not in self._filters:
                for _id in characters[character]["id"]:
                    location = first + (_id * total_bytes) + offset
                    self._rom_data[location] = 0
                    self._rom_data[location + 1] = 0
