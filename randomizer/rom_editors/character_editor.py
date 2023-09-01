""" Base class for editing characters """

from random import randint

from constants import CLASS_MODE_STAFF, CLASS_MODE_ALL
from rom_editors.item_editor import ItemEditor, WEAPON_MAP


class CharacterEditor:
    """CharacterEditor base class"""

    def __init__(self, game_config, rom_data, class_mode, mix_promotes):
        self._game_config = game_config
        self._rom_data = rom_data
        self._class_mode = class_mode
        self._mix_promotes = mix_promotes

        self._filters = []

        self._item_editor = ItemEditor(self._rom_data, self._game_config)

    def set_filters(self, filters):
        """Set the filters for randomization"""
        self._filters = filters

    @property
    def rom_data(self):
        """Make rom_data read only. Should only modify things one at a time"""
        return self._rom_data

    def handle_overrides(self):
        """Sub-classes can perform overrides after randomization"""

    def randomize(self):
        """Randomize based on the current status of the CONFIG"""
        promoted, unpromoted = self._get_class_list()

        for character in self._game_config.characters:
            if character.kind not in self._filters:
                new_class = self.get_new_class(promoted, unpromoted, character)
                for char_class in character.location:
                    self._rom_data[char_class] = new_class

                self.update_weapon_type(new_class, character.id)
                weapon_type = self.get_weapon_type_for_class(new_class)
                self._item_editor.load(character.item_pos, new_class, weapon_type)
                self._item_editor.randomize()

        self.randomize_palettes()
        self.add_promotions()
        self.fix_flyers()

        self.handle_overrides()
        self._item_editor.handle_overrides()

        return self._rom_data

    def get_new_class(self, promoted, unpromoted, character):
        """Get a randomized class based on specs"""
        if self._mix_promotes:
            class_list = promoted + unpromoted
        elif any(
            character.id[idx]
            for idx, class_id in enumerate(character.id)
            if class_id in self._game_config.char_stats.promotion_overrides
        ):
            class_list = promoted
        else:
            class_list = (
                promoted
                if self._get_current_class(character.id[0]) in promoted
                else unpromoted
            )

        return class_list[randint(0, len(class_list) - 1)]

    def get_weapon_type_for_class(self, new_class):
        """
        Get weapon type for that class. This should be the highest weapon lvl on all
        weapons in the base class
        """
        type_ = "dragonstone/monster"
        highest = 0
        weapon_pos = (
            self._game_config.class_stats.first
            + self._game_config.class_stats.offsets.weapon
            + (self._game_config.sizes.class_ * new_class)
        )

        for weapon_idx in range(8):
            # If staff is not their only choice use a different weapon
            if (
                weapon_idx == 4
                and new_class not in self._game_config.class_stats.staff_only
            ):
                continue

            weapon_lvl = self._rom_data[weapon_pos + weapon_idx]
            if weapon_lvl > highest:
                highest = weapon_lvl
                type_ = WEAPON_MAP[weapon_idx]

        return type_

    def _get_current_class(self, char_id):
        """Get the current class of {char_id}"""
        first = self._game_config.char_stats.first
        offset = self._game_config.char_stats.offsets.class_
        location = first + (self._game_config.sizes.character * char_id) + offset
        return self._rom_data[location]

    def _get_class_list(self):
        promoted = []
        unpromoted = []
        first_class = self._game_config.class_stats.first

        # Start at negative value and increment at beginning of loop
        class_ptr = 0 - self._game_config.sizes.class_
        for _class in range(self._game_config.totals.class_):
            class_ptr += self._game_config.sizes.class_

            if _class in self._game_config.class_stats.blacklist:
                continue

            if (
                _class in self._game_config.class_stats.other
                and self._class_mode != CLASS_MODE_ALL
            ):
                continue

            if (
                _class in self._game_config.class_stats.staff_only
                and self._class_mode
                not in [
                    CLASS_MODE_ALL,
                    CLASS_MODE_STAFF,
                ]
            ):
                continue

            prom_pos = self._rom_data[
                first_class
                + class_ptr
                + self._game_config.class_stats.offsets.promotion
            ]
            if int(prom_pos) & self._game_config.class_stats.bit_masks.promotion == 0:
                unpromoted.append(_class)

            else:
                promoted.append(_class)

        return promoted, unpromoted

    def update_weapon_type(self, new_class, ids):
        """Get the character by their IDs. Use that to get their current weapon lvl"""
        for id_ in ids:
            highest = 0
            character_pos = self._game_config.char_stats.first + (
                self._game_config.sizes.character * id_
            )

            for weapon_idx in range(8):
                weapon_lvl = self._rom_data[
                    character_pos
                    + self._game_config.char_stats.offsets.weapon
                    + weapon_idx
                ]
                if weapon_lvl > highest:
                    highest = weapon_lvl

                # Zero out the weapon lvl
                self._rom_data[
                    character_pos
                    + self._game_config.char_stats.offsets.weapon
                    + weapon_idx
                ] = 0
            if highest == 0:
                highest = self._game_config.items.a_weapon_lvl

            self._set_weapon_levels_for_class(highest, character_pos, new_class)

    def _set_weapon_levels_for_class(self, weapon_lvl, character_pos, new_class):
        # Get position of class to determine what weapons apply to this class
        class_pos = self._game_config.class_stats.first + (
            self._game_config.sizes.class_ * new_class
        )
        offsets = [
            idx
            for idx in range(8)
            if self._rom_data[
                class_pos + self._game_config.class_stats.offsets.weapon + idx
            ]
            != 0
        ]

        # Set offsets for character based on class
        for offset in offsets:
            self._rom_data[
                character_pos + self._game_config.char_stats.offsets.weapon + offset
            ] = weapon_lvl

    def randomize_palettes(self):
        """Randomize the character palettes based on filters"""
        for character in self._game_config.characters:
            if character.kind not in self._filters:
                for _id in character.id:
                    for offset in {
                        self._game_config.palette_stats.offsets.base,
                        self._game_config.palette_stats.offsets.promo,
                    }:
                        rand = randint(0, self._game_config.totals.palettes - 1)
                        self._rom_data[
                            self._game_config.char_stats.first
                            + (_id * self._game_config.sizes.character)
                            + offset
                        ] = rand

    def add_promotions(self):
        """Add promotion classes to classes that don't have promotions"""
        for override in self._game_config.class_stats.promotion.overrides:
            self._rom_data[
                self._game_config.class_stats.first
                + (override.unprom_class * self._game_config.sizes.class_)
                + self._game_config.char_stats.offsets.class_
            ] = override.prom_class

    def fix_flyers(self):
        """
        When certain units who were flying get randomized into ground units, it can
        break the game if the cutscene calls for flying over mountains or water. These
        tweaks start the unit into terrain tiles that will allow safe navigation to
        their destination.
        """
        for override in self._game_config.char_stats.overrides.flyers:
            self._rom_data[override.address] = override.byte

    def _get_character_by_name(self, name):
        for character in self._game_config.characters:
            if character.name == name:
                return character

        raise ValueError(f"No known character named: {name}")
