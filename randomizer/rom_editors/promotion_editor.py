""" Module for editing promotions and promotional items """


class PromotionEditor:
    """ Base PromotionEditor class """

    def __init__(self, game_config, rom_data):
        self._game_config = game_config
        self._rom_data = rom_data

    @property
    def rom_data(self):
        """ Make rom_data read only. Should only modify things one at a time """
        return self._rom_data

    def make_all_master_seals(self):
        """ Change the appearance of all promotion items to master seals """
        offsets = self._game_config["items"]["offsets"]
        prom_config = self._game_config["items"]["promotional"]
        for prom_item in prom_config["items"]:
            location = prom_config["items"][prom_item]["item_location"]
            self._do_single_byte_categories(offsets, location)
            self._do_multi_bytes_categories(offsets, location)

        return self._rom_data

    def add_classes_to_promotion(self):
        """ Override the method because we need to allocate and use a different space """
        prom_items = self._game_config["items"]["promotional"]["items"]
        classes_to_add = self._game_config["items"]["promotional"]["classes_to_add"]
        for item in prom_items:
            new_loc = prom_items[item]["new_location"]
            # Set the pointers to the new location
            for pointer in prom_items[item]["pointers"]:
                loc_bytes = parse_pointer(new_loc)

                for idx, _ in enumerate(loc_bytes):
                    self._rom_data[pointer + idx] = loc_bytes[idx]

            # Set classes in new location
            for idx, _ in enumerate(classes_to_add):
                self._rom_data[new_loc + idx] = classes_to_add[idx]

            # Write a zero at the ned to signal end of class list
            self._rom_data[new_loc + len(classes_to_add)] = 0

    def _do_multi_bytes_categories(self, offsets, location):
        """ Set the multiple byte attributes for this promotion item """
        for category in {"name", "description", "use_screen"}:
            for idx in range(len(self._game_config["items"]["master_seal"][category])):
                self._rom_data[location + offsets[category] + idx] = self._game_config[
                    "items"
                ]["master_seal"][category][idx]

    def _do_single_byte_categories(self, offsets, location):
        """ Set the single byte attributes for this promotion item """
        for category in {"icon", "use"}:
            self._rom_data[location + offsets[category]] = self._game_config["items"][
                "master_seal"
            ][category]


def parse_pointer(pointer):
    """ Return the 3 bytes that make up the pointer in reversed order (little endian) """
    str_repr = str(hex(pointer)).split("x")[1]
    assert (
        len(str_repr) == 6
    ), f"New location should only be 3 bytes. Was actually {str_repr}"
    return int(str_repr[-2:], 16), int(str_repr[2:4], 16), int(str_repr[:2], 16)
