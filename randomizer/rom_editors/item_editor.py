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
        self._weapon = None

        self._class_stats = game_config["classes"]["class_stats"]

        # Set flux to E rank
        rom_data[game_config["items"]["flux_weapon_lvl_pos"]] = 1

    def randomize(self):
        """ Randomize all items in {item_pos} """
        prf_weapons = self._game_config["items"]["prf"]
        for item_pos in self._item_pos:
            self.randomize_item(item_pos, prf_weapons)

    def randomize_item(self, item_pos, prf_weapons):
        """ Randomize the specific item """
        if self._new_class == self._class_stats["manakete"]:
            self._rom_data[item_pos] = self._game_config["items"]["dragonstone"]
            return

        item = self._rom_data[item_pos]
        if item in prf_weapons:
            item = self.handle_prf(item)

        # Handle case where we want to auto assign an iron sword
        if item == 0:
            item = 1

        item_type = self._get_item_type(item)
        item_lvl = self._get_item_lvl(item, item_type)

        # This list gets modified. Make sure we copy it first
        weapon_list = list(self._game_config["items"][item_lvl][self._weapon])

        # If not ranged monster, take out ranged monster items
        if (
            self._rom_data[self._class_pos + self._class_stats["id_offset"]]
            not in self._class_stats["ranged_monster"]
        ):
            for weapon in list(weapon_list):
                if weapon in self._game_config["items"]["ranged_monster"]:
                    weapon_list.remove(weapon)

        rand = randint(0, len(weapon_list) - 1)
        self._rom_data[item_pos] = weapon_list[rand]

    def handle_prf(self, item):
        """ Wipe the locks to characters on this item """
        raise NotImplementedError("Classes must override this method")

    @property
    def rom_data(self):
        """ Make rom_data read only. Should only modify things one at a time """
        return self._rom_data

    def load(self, item_pos, class_, weapon):
        """ Load the new character's items """
        class_stats = self._game_config["classes"]["class_stats"]
        self._class_pos = class_stats["first"] + (class_ * class_stats["total_bytes"])
        self._item_pos = item_pos
        self._weapon = weapon
        self._new_class = class_

    def _get_item_lvl(self, item, item_type):
        """ Return the lvl this weapon is (e, d, c ... etc) """
        for level in {"e", "d", "c", "b", "a"}:
            if item in self._game_config["items"][level][item_type]:
                return level

        raise ItemException("Could not determine level of item {item}")

    def _get_item_type(self, item):
        """ Return the item type """

        for _type in self._game_config["items"]["types"].values():
            if item in self._get_items(_type):
                return _type

        raise ItemNotFoundException(f"No known item {hex(item)}")

    def _get_items(self, item_type):
        """ Return all items of that type """
        items = []
        for level in {"e", "d", "c", "b", "a"}:
            items += self._game_config["items"][level][item_type]

        return items
