""" Module for editing characters """

from random import randint

from constants import CLASS_MODE_STAFF, CLASS_MODE_ALL

from rom_editors.item_editor import ItemEditor, WEAPON_MAP


class CharacterEditor:
    """ CharacterEditor class """

    def __init__(self, game_config, rom_data, class_mode, mix_promotes):
        self._game_config = game_config
        self._rom_data = rom_data
        self._class_mode = class_mode
        self._mix_promotes = mix_promotes

        self._filters = []

        self._class_stats = game_config["classes"]["class_stats"]
        self._character_stats = game_config["classes"]["character_stats"]

    def set_filters(self, filters):
        """ Set the filters for randomization """
        self._filters = filters

    def randomize(self):
        """ Randomize based on the current status of the CONFIG """
        promoted, unpromoted = self._get_class_list()
        class_list = []

        item_editor = ItemEditor(self._rom_data, self._game_config)
        for character in self._game_config["classes"]["characters"]:
            character_data = self._game_config["classes"]["characters"][character]
            if character_data["kind"] not in self._filters:

                if self._mix_promotes:
                    class_list = promoted + unpromoted
                else:
                    class_list = (
                        promoted
                        if self._rom_data[character_data["location"][0]] in promoted
                        else unpromoted
                    )

                new_class = class_list[randint(0, len(class_list) - 1)]
                char_classes = character_data["location"]

                self._update_weapon_type(new_class, character_data["id"])
                weapon = self._get_weapon_for_class(new_class)

                # Randomize the class
                for char_class in char_classes:
                    self._rom_data[char_class] = new_class

                item_editor.load(character_data["item_pos"], new_class, weapon)
                item_editor.randomize()

        return self._rom_data

    def _get_weapon_for_class(self, new_class):
        """Get weapon for that class. This should be the highest weapon lvl on all weapons
        in the base class
        """
        weapon = "dragonstone/monster"
        highest = 0
        weapon_pos = (
            self._class_stats["first"]
            + self._class_stats["weapon_offset"]
            + (self._class_stats["total_bytes"] * new_class)
        )

        for weapon_idx in range(8):
            # If staff is not their only choice use a different weapon
            if weapon_idx == 4 and new_class not in self._class_stats["staff_only"]:
                continue

            weapon_lvl = self._rom_data[weapon_pos + weapon_idx]
            if weapon_lvl > highest:
                highest = weapon_lvl
                weapon = WEAPON_MAP[weapon_idx]

        return weapon

    def _update_weapon_type(self, new_class, ids):
        """ Get the character by their IDs. Use that to get their current weapon lvl """
        for id_ in ids:
            highest = 0
            character_pos = self._character_stats["first"] + (
                self._character_stats["total_bytes"] * id_
            )

            for weapon_idx in range(8):
                weapon_lvl = self._rom_data[
                    character_pos + self._character_stats["weapon_offset"] + weapon_idx
                ]
                if weapon_lvl > highest:
                    highest = weapon_lvl

                # Zero out the weapon lvl
                self._rom_data[
                    character_pos + self._character_stats["weapon_offset"] + weapon_idx
                ] = 0

            if highest == 0:
                highest = self._game_config["items"]["a_weapon_lvl"]

            self._set_weapon_levels_for_class(highest, character_pos, new_class)

    def _set_weapon_levels_for_class(self, weapon_lvl, character_pos, new_class):
        # Get position of class to determine what weapons apply to this class
        class_pos = self._class_stats["first"] + (
            self._class_stats["total_bytes"] * new_class
        )
        offsets = [
            idx
            for idx in range(8)
            if self._rom_data[class_pos + self._class_stats["weapon_offset"] + idx] != 0
        ]

        # Set offsets for character based on class
        for offset in offsets:
            self._rom_data[
                character_pos + self._character_stats["weapon_offset"] + offset
            ] = weapon_lvl

    def _get_class_list(self):
        promoted = []
        unpromoted = []
        class_ptr = 0

        first_class = self._class_stats["first"]
        for _class in range(self._class_stats["num_classes"]):
            if _class in self._class_stats["blacklist"]:
                class_ptr += self._class_stats["total_bytes"]
                continue

            if (
                _class in self._class_stats["other"]
                and self._class_mode != CLASS_MODE_ALL
            ):
                class_ptr += self._class_stats["total_bytes"]
                continue

            if _class in self._class_stats["staff_only"] and self._class_mode not in [
                CLASS_MODE_ALL,
                CLASS_MODE_STAFF,
            ]:
                class_ptr += self._class_stats["total_bytes"]
                continue

            prom_pos = self._rom_data[
                first_class + class_ptr + self._class_stats["promotion"]["offset"]
            ]
            if int(prom_pos) & self._class_stats["promotion"]["bit_mask"] == 0:
                unpromoted.append(_class)

            else:
                promoted.append(_class)

            class_ptr += self._class_stats["total_bytes"]

        return promoted, unpromoted
