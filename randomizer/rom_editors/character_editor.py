""" Base class for editing characters """

from random import randint

from constants import CLASS_MODE_STAFF, CLASS_MODE_ALL
from rom_editors.item_editor import ItemEditor, WEAPON_MAP


class CharacterEditor:
    """ CharacterEditor base class """

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

    @property
    def rom_data(self):
        """ Make rom_data read only. Should only modify things one at a time """
        return self._rom_data

    def randomize(self):
        """ Randomize based on the current status of the CONFIG """
        promoted, unpromoted = self._get_class_list()
        characters = self._game_config["classes"]["characters"]
        banned_promotes = self._character_stats["promotion_overrides"]
        class_list = []

        item_editor = ItemEditor(self._rom_data, self._game_config)
        for character in characters:
            character_data = characters[character]
            if character_data["kind"] not in self._filters:
                if self._mix_promotes:
                    class_list = promoted + unpromoted

                elif any(
                    characters[character]["id"][idx]
                    for idx, _id in enumerate(characters[character]["id"])
                    if _id in banned_promotes
                ):
                    class_list = promoted
                else:
                    class_list = (
                        promoted
                        if self._rom_data[character_data["location"][0]] in promoted
                        else unpromoted
                    )

                new_class = class_list[randint(0, len(class_list) - 1)]
                self._update_weapon_type(new_class, character_data["id"])
                weapon = self._get_weapon_for_class(new_class)

                # Randomize the class
                for char_class in character_data["location"]:
                    self._rom_data[char_class] = new_class

                item_editor.load(character_data["item_pos"], new_class, weapon)
                item_editor.randomize()

        self._randomize_palettes()

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

    def _randomize_palettes(self):
        """ Randomize the character palettes based on filters """
        # Need to override the method because FE8 treats palettes differently
        characters = self._game_config["classes"]["characters"]
        palette_stats = self._game_config["classes"]["palette_stats"]
        prom_stats = self._game_config["classes"]["promotion_stats"]
        for character in characters:
            if characters[character]["kind"] not in self._filters:
                for _id in characters[character]["id"]:
                    # Randomize all palettes
                    pos = palette_stats["first_palette"] + (
                        palette_stats["total_bytes"] * _id
                    )
                    for idx in range(palette_stats["total_bytes"]):
                        rand = randint(0, palette_stats["num_palettes"])
                        self._rom_data[pos + idx] = rand

                    # Set palette classes to newly randomized classes
                    # Use both promotion 1 and promotion 2. If unit does not promote,
                    # Both values also get set to 0

                    # Use the first character location to get the new class
                    new_class = self._rom_data[characters[character]["location"][0]]

                    # Set base class first
                    pos = (
                        palette_stats["first_class"]
                        + (palette_stats["total_bytes"] * _id)
                        + palette_stats["base_class_offset"]
                    )
                    self._rom_data[pos] = new_class

                    # Set the 2 promotion classes
                    pos = (
                        palette_stats["first_class"]
                        + (palette_stats["total_bytes"] * _id)
                        + palette_stats["promoted_class_offset"]
                    )
                    new_prom_class = prom_stats["first"] + (
                        prom_stats["total_bytes"] * new_class
                    )
                    for idx in range(palette_stats["num_promoted_classes"]):
                        self._rom_data[pos + idx] = self._rom_data[new_prom_class + idx]

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
