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

        self._item_editor = ItemEditor(self._rom_data, self._game_config)

    def set_filters(self, filters):
        """ Set the filters for randomization """
        self._filters = filters

    @property
    def rom_data(self):
        """ Make rom_data read only. Should only modify things one at a time """
        return self._rom_data

    def handle_overrides(self):
        """ Sub-classes can perform overrides after randomization """

    def handle_promotion_targets(self):
        """ Sub-classes can change promotion targets for the class """

    def randomize(self):
        """ Randomize based on the current status of the CONFIG """
        promoted, unpromoted = self._get_class_list()
        characters = self._game_config["classes"]["characters"]

        for character in characters:
            character_data = characters[character]
            if characters[character]["kind"] not in self._filters:
                new_class = self.get_new_class(promoted, unpromoted, character_data)
                for char_class in character_data["location"]:
                    self._rom_data[char_class] = new_class

                self.update_weapon_type(new_class, character_data["id"])
                weapon = self.get_weapon_for_class(new_class)
                self._item_editor.load(character_data["item_pos"], new_class, weapon)
                self._item_editor.randomize()

        self._item_editor.handle_prf()
        self._item_editor.handle_s_rank()

        self.randomize_palettes()
        self.add_promotions()

        self.handle_overrides()
        self.handle_promotion_targets()

        return self._rom_data

    def get_new_class(self, promoted, unpromoted, character_data):
        """ Get a randomized class based on specs """
        character_stats = self._game_config["classes"]["character_stats"]
        if self._mix_promotes:
            class_list = promoted + unpromoted
        elif any(
            character_data["id"][idx]
            for idx, class_id in enumerate(character_data["id"])
            if class_id in character_stats["promotion_overrides"]
        ):
            class_list = promoted
        else:
            class_list = (
                promoted
                if self._rom_data[character_data["location"][0]] in promoted
                else unpromoted
            )

        return class_list[randint(0, len(class_list) - 1)]

    def get_weapon_for_class(self, new_class):
        """
        Get weapon for that class. This should be the highest weapon lvl on all weapons
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

    def _get_class_list(self):
        promoted = []
        unpromoted = []
        first_class = self._class_stats["first"]

        # Start at negative value and increment at beginning of loop
        class_ptr = 0 - self._class_stats["total_bytes"]
        for _class in range(self._class_stats["num_classes"]):
            class_ptr += self._class_stats["total_bytes"]

            if _class in self._class_stats["blacklist"]:
                continue

            if (
                _class in self._class_stats["other"]
                and self._class_mode != CLASS_MODE_ALL
            ):
                continue

            if _class in self._class_stats["staff_only"] and self._class_mode not in [
                CLASS_MODE_ALL,
                CLASS_MODE_STAFF,
            ]:
                continue

            prom_pos = self._rom_data[
                first_class + class_ptr + self._class_stats["promotion"]["offset"]
            ]
            if int(prom_pos) & self._class_stats["promotion"]["bit_mask"] == 0:
                unpromoted.append(_class)

            else:
                promoted.append(_class)

        return promoted, unpromoted

    def update_weapon_type(self, new_class, ids):
        """ Get the character by their IDs. Use that to get their current weapon lvl """
        character_stats = self._game_config["classes"]["character_stats"]
        for id_ in ids:
            highest = 0
            character_pos = character_stats["first"] + (
                character_stats["total_bytes"] * id_
            )

            for weapon_idx in range(8):
                weapon_lvl = self._rom_data[
                    character_pos + character_stats["weapon_offset"] + weapon_idx
                ]
                if weapon_lvl > highest:
                    highest = weapon_lvl

                # Zero out the weapon lvl
                self._rom_data[
                    character_pos + character_stats["weapon_offset"] + weapon_idx
                ] = 0
            if highest == 0:
                highest = self._game_config["items"]["a_weapon_lvl"]

            self._set_weapon_levels_for_class(highest, character_pos, new_class)

    def _set_weapon_levels_for_class(self, weapon_lvl, character_pos, new_class):
        character_stats = self._game_config["classes"]["character_stats"]
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
                character_pos + character_stats["weapon_offset"] + offset
            ] = weapon_lvl

    def randomize_palettes(self):
        """ Randomize the character palettes based on filters """
        character_stats = self._game_config["classes"]["character_stats"]
        characters = self._game_config["classes"]["characters"]
        palette_stats = self._game_config["classes"]["palette_stats"]
        for character in characters:
            if characters[character]["kind"] not in self._filters:
                for _id in characters[character]["id"]:
                    for offset in {
                        palette_stats["base_offset"],
                        palette_stats["promo_offset"],
                    }:
                        rand = randint(0, palette_stats["num_palettes"] - 1)
                        self._rom_data[
                            character_stats["first"]
                            + (_id * character_stats["total_bytes"])
                            + offset
                        ] = rand

    def add_promotions(self):
        """ Add promotion classes to classes that don't have promotions """
        for _id, _class in self._class_stats["promotion"]["overrides"].items():
            self._rom_data[
                self._class_stats["first"]
                + (_id * self._class_stats["total_bytes"])
                + self._game_config["classes"]["character_stats"]["class_offset"]
            ] = _class
