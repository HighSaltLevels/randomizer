""" FE7 Override Class for editing characters """

from random import randint

from rom_editors.character_editor import CharacterEditor
from rom_editors.fe7.item_editor import FE7ItemEditor


class FE7CharacterEditor(CharacterEditor):
    """ FE7 Override to override the ItemEditor """

    def __init__(self, game_config, rom_data, class_mode, mix_promotes):
        super().__init__(game_config, rom_data, class_mode, mix_promotes)
        # Override the item editor
        self._item_editor = FE7ItemEditor(self._rom_data, self._game_config)

    def handle_overrides(self):
        """ Do all FE7-specific overrides """
        self._handle_serra_override()
        self._handle_thief_override()
        self._handle_teodor_override()
        self._handle_karla_override()
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
        offset = 0x11
        serra = self._get_character_by_name("Serra")
        first = self._game_config.char_stats.first
        size = self._game_config.sizes.character
        for id_ in serra.id:
            self._rom_data[first + (id_ * size) + offset] = 0

    def _handle_thief_override(self):
        """
        Although a thief is not required to complete chapter 6, starting Matthew
        with an additional door key and chest key will allow the player to get
        all loot.

        Additionally, if Legault does not have chest keys, he will immediately leave
        the Dragon's Gate chapter. So we should give him chest keys as well
        """
        matthew = self._get_character_by_name("Matthew")
        for item_pos in matthew.extra_item_pos:
            self._rom_data[item_pos] = self._game_config.items.chest_key_id
            self._rom_data[item_pos + 1] = self._game_config.items.door_key_id

        legault = self._get_character_by_name("Legault")
        for item_pos in legault.extra_item_pos:
            self._rom_data[item_pos] = self._game_config.items.chest_key_id

    def _handle_teodor_override(self):
        """
        Replace the generic Druid that's holding Gespenst with the character
        Teodor.
        """
        teodor_id = self._get_character_by_name("Teodor").id[0]
        self._rom_data[
            self._game_config.char_stats.overrides.generic_druid_pos
        ] = teodor_id

    def _handle_karla_override(self):
        """
        Karla only appears on Hector mode if Bartre is a level 5 Warrior. If Bartre
        is randomized to any other class than fighter, then it is impossible for
        Karla to even appear. So let's overwrite the branch statments that will skip
        loading Karla in with NO-OP statements so that she always spawns in.
        """
        for address in self._game_config.char_stats.overrides.noops:
            self._rom_data[address] = 0

    def _give_final_bosses_s_ranks(self):
        """
        Now that final bosses have s rank weapons, we need to go in and give them
        the proper weapon lvls for those s ranks
        """
        for boss in self._game_config.char_stats.final_bosses:
            # First get the weapon type. then use it to grab an appropriate
            # S rank item
            character = self._get_character_by_name(boss)
            weapon_id = self._rom_data[character.s_rank_locations[0]]
            weapon_type = self._rom_data[
                self._game_config.items.first
                + (weapon_id * self._game_config.sizes.item)
                + self._game_config.items.offsets.type
            ]

            for char_id in character.id:
                self._rom_data[
                    self._game_config.char_stats.first
                    + (char_id * self._game_config.sizes.character)
                    + self._game_config.char_stats.offsets.weapon
                    + weapon_type
                ] = self._game_config.items.s_weapon_lvl

    def _make_weapons_dropable(self):
        """
        Make Nergal's, Morph Linus's, and Morph Jerme's weapons dropable.
        It's done through changing a bit on ability 4 on the character.
        """
        for _id in self._game_config.char_stats.dropable_weapon_characters:
            first = self._game_config.char_stats.first
            offset = (
                self._game_config.sizes.character * _id
            ) + self._game_config.char_stats.offsets.ability4
            self._rom_data[first + offset] = (
                self._rom_data[first + offset]
                | self._game_config.char_stats.offsets.dropable_bitmask
            )

    def _remove_hardcoded_animations(self):
        """
        Some characters are given hardcoded animations. Let's remove them
        """
        first = self._game_config.char_stats.first
        total_bytes = self._game_config.sizes.character
        offset = self._game_config.char_stats.offsets.animation
        for character in self._game_config.characters:
            if character.kind not in self._filters:
                for _id in character.id:
                    location = first + (_id * total_bytes) + offset
                    self._rom_data[location] = 0
                    self._rom_data[location + 1] = 0

    def _get_character_by_name(self, name):
        for character in self._game_config.characters:
            if character.name == name:
                return character

        raise ValueError(f"No known character named: {name}")
