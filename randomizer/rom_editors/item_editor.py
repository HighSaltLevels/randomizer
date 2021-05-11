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

        self._class_pos = None
        self._item_pos = None
        self._weapon = None

        # Set flux to E rank
        rom_data[game_config["items"]["flux_weapon_lvl_pos"]] = 1

    def randomize(self):
        """ Randomize all items in {item_pos} """
        prf_weapons = self._game_config["items"]["prf"]
        for item_pos in self._item_pos:
            item = self._rom_data[item_pos]

            if item in prf_weapons:
                item = self._swap_prf(item)

            # Handle case where we want to auto assign an iron sword
            if item == 0:
                item = 1

            if (
                self._class_pos
                == self._game_config["classes"]["class_stats"]["manakete_pos"]
            ):
                self._rom_data[item_pos] = self._game_config["items"]["dragonstone"]

            else:
                item_type = self._get_item_type(item)
                item_lvl = self._get_item_lvl(item, item_type)
                weapon_list = self._game_config["items"][item_lvl][self._weapon]
                rand = randint(0, len(weapon_list) - 1)
                self._rom_data[item_pos] = weapon_list[rand]

    def load(self, item_pos, class_, weapon):
        """ Load the new character's items """
        class_stats = self._game_config["classes"]["class_stats"]
        self._class_pos = self._rom_data[
            class_stats["first"] + (class_ * class_stats["total_bytes"])
        ]
        self._item_pos = item_pos
        self._weapon = weapon

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

        raise ItemNotFoundException(f"No known item {item}")

    def _swap_prf(self, item):
        """ Swap prf weapon for equivalent rank weapon """
        item_eq_dict = {
            self._game_config["items"]["rapier"]: 1,  # E rank sword
            self._game_config["items"]["reginleif"]: 22,  # D rank lance
            self._game_config["items"]["naglfar"]: 73,  # A rank dark
        }

        return item_eq_dict[item]

    def _get_items(self, item_type):
        """ Return all items of that type """
        items = []
        for level in {"e", "d", "c", "b", "a"}:
            items += self._game_config["items"][level][item_type]

        return items


def make_all_master_seals(game_config, rom_data):
    """ Change all promotion items to master seals """
    offsets = game_config["items"]["offsets"]
    for prom_item in game_config["items"]["promotional"]:
        for category in {"name", "description", "use_screen"}:
            for idx in range(2):
                location = prom_item + offsets[category]
                rom_data[location + idx] = game_config["items"]["master_seal"][
                    category
                ][idx]

        for category in {"icon", "use"}:
            rom_data[prom_item + offsets[category]] = game_config["items"][
                "master_seal"
            ][category]

    return rom_data
