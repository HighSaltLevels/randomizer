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
            self.do_single_byte_categories(offsets, location)
            self.do_multi_bytes_categories(offsets, location)

        return self._rom_data

    def do_single_byte_categories(self, offsets, location):
        """ Set the single byte attributes for this promotion item """
        for category in {"icon", "use"}:
            self._rom_data[location + offsets[category]] = self._game_config["items"][
                "master_seal"
            ][category]

    def do_multi_bytes_categories(self, offsets, location):
        """ Set the multiple byte attributes for this promotion item """
        for category in {"name", "description", "use_screen"}:
            for idx in range(len(self._game_config["items"]["master_seal"][category])):
                self._rom_data[location + offsets[category] + idx] = self._game_config[
                    "items"
                ]["master_seal"][category][idx]
