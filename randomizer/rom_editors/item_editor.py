""" Module for editing items """

from random import randint


WEAPON_MAP = {
    0: "sword",
    1: "lance",
    2: "axe",
    3: "bow",
    4: "staff",
    5: "anima",
    6: "light",
    7: "dark",
    8: "dragonstone/monster",
}


class ItemException(Exception):
    """ Raised when there is an unexpected error handling items """


class ItemNotFoundException(ItemException):
    """ Raised when there is an unexpected item is not in config """


class ItemEditor:
    """ Item Editor class """

    def __init__(self, rom_data, game_config):
        self._rom_data = rom_data
        self._game_config = game_config

        self._new_class = None
        self._class_pos = None
        self._item_pos = None
        self._weapon_type = None

        # Set flux to E rank
        rom_data[game_config.items.flux_weapon_lvl_pos] = 1

    def randomize(self):
        """ Randomize all items in {item_pos} """
        for item_pos in self._item_pos:
            self.randomize_item(item_pos)

    def randomize_item(self, item_pos):
        """ Randomize the specific item """
        if self._new_class == self._game_config.class_stats.manakete:
            self._rom_data[item_pos] = self._game_config.items.dragonstone
            return

        # For FE6 only. Check if it's Fae's class
        if self._new_class == self._game_config.class_stats.manakete_f:
            self._rom_data[item_pos] = self._game_config.items.divinestone
            return

        item = self._rom_data[item_pos]

        # If the current item is 0, that means that item slot is unused.
        # When the spec specifies an unused item location, assume equivalent
        # item is an iron sword.
        if item == 0:
            item = 1

        # If it's a prf item, replace it with an equivalent common item
        for prf in self._game_config.items.prfs:
            if item == prf.weapon:
                item = prf.equivalent
                break

        # Get the current item type and use that to find its rank
        curr_item_type = self._get_item_type(item)
        rank = self._get_item_rank(curr_item_type)

        # Use the rank and updated weapon type to create a weapon list
        weapon_list = self._create_weapon_list(rank, self._weapon_type)

        # If not ranged monster, take out ranged monster items
        if (
            self._rom_data[self._class_pos + self._game_config.class_stats.offsets.id]
            not in self._game_config.class_stats.ranged_monster
        ):
            for weapon in list(weapon_list):
                if weapon in self._game_config.items.ranged_monster:
                    weapon_list.remove(weapon)

        rand = randint(0, len(weapon_list) - 1)
        self._rom_data[item_pos] = weapon_list[rand]

    def handle_overrides(self):
        """ Sub-classes can optionally do extra operations on items """

    @property
    def rom_data(self):
        """ Make rom_data read only. Should only modify things one at a time """
        return self._rom_data

    def load(self, item_pos, class_, weapon_type):
        """ Load the new character's items """
        self._class_pos = self._game_config.class_stats.first + (
            class_ * self._game_config.sizes.class_
        )
        self._item_pos = item_pos
        self._weapon_type = weapon_type
        self._new_class = class_

    def _get_item_rank(self, item_type):
        """ Look up the rank for this weapon is (e, d, c ... etc) """
        for weapon in self._game_config.items.weapons:
            if weapon.type == item_type:
                return weapon.rank

        raise ItemException("Could not determine rank of item {hex(item)}")

    def _get_item_type(self, item):
        """ Return the item type """
        for weapon in self._game_config.items.weapons:
            if item in weapon.list_:
                return weapon.type

        raise ItemNotFoundException(f"No known item {hex(item)}")

    def _create_weapon_list(self, rank, item_type):
        """ Return the weapon list corresponding to the rank and item_type """
        for weapon in self._game_config.items.weapons:
            if weapon.rank == rank and weapon.type == item_type:
                return weapon.list_

        raise ItemException(
            "Could not find suitable match for rank {rank} and type {item_type} weapons"
        )
