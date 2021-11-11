""" Override Module for editing items in FE7 """

from random import randint

from rom_editors.item_editor import ItemEditor


class FE7ItemEditor(ItemEditor):
    """ FE8 Item Editor """

    def handle_prf(self, item_idx):
        """
        Swap prf weapon for equivalent rank weapon.
        Also, zero out item locks
        """
        first_item = self._game_config["items"]["first"]
        total_bytes = self._game_config["items"]["total_bytes"]
        self._rom_data[
            self._game_config["items"]["offsets"]["ability3"]
            + (item_idx * total_bytes)
            + first_item
        ] = 0
        item_eq_dict = {
            self._game_config["items"]["rapier"]: 1,  # E rank sword
            self._game_config["items"]["mani_katti"]: 1,  # E rank sword
            self._game_config["items"]["forblaze"]: 59,  # A rank anima
            self._game_config["items"]["durandal"]: 4,  # A rank sword
            self._game_config["items"]["armads"]: 33,  # A rank axe
            self._game_config["items"]["sol_katti"]: 4,  # A rank sword
            self._game_config["items"]["wolf_beil"]: 31,  # E rank dark
            self._game_config["items"]["ereshkigal"]: 48,  # A rank dark
            self._game_config["items"]["regal_blade"]: 4,  # A rank sword
            self._game_config["items"]["rex_hasta"]: 23,  # A rank lance
            self._game_config["items"]["basilikos"]: 33,  # A rank axe
            self._game_config["items"]["rienfleche"]: 46,  # A rank bow
            self._game_config["items"]["excalibur"]: 59,  # A rank anima
            self._game_config["items"]["luce"]: 66,  # A rank light
            self._game_config["items"]["gespenst"]: 48,  # A rank dark
        }

        return item_eq_dict[item_idx]

    def handle_game_specific_configs(self):
        self._assign_s_ranks()

    def _assign_s_ranks(self):
        """ Give all bosses in final chapter s rank weapons """
        item_eq_dict = {
            "sword": [
                self._game_config["items"]["durandal"],
                self._game_config["items"]["sol_katti"],
                self._game_config["items"]["regal_blade"],
            ],
            "lance": [
                self._game_config["items"]["rex_hasta"],
            ],
            "axe": [
                self._game_config["items"]["armads"],
                self._game_config["items"]["basilikos"],
            ],
            "bow": [
                self._game_config["items"]["rienfleche"],
            ],
            "staff": [0x4E],  # Just give them a Fortify staff
            "anima": [
                self._game_config["items"]["forblaze"],
                self._game_config["items"]["excalibur"],
            ],
            "light": [
                self._game_config["items"]["luce"],
                self._game_config["items"]["aureola"],
            ],
            "dark": [
                self._game_config["items"]["ereshkigal"],
                self._game_config["items"]["gespenst"],
            ],
        }
        for boss in self._game_config["classes"]["character_stats"]["final_bosses"]:
            for item_loc in self._game_config["classes"]["characters"][boss][
                "s_rank_locations"
            ]:
                item = self._rom_data[item_loc]
                item_type = self._get_s_item_type(item)
                rand = randint(0, len(item_eq_dict[item_type]) - 1)
                self._rom_data[item_loc] = item_eq_dict[item_type][rand]

    def _get_s_item_type(self, item_idx):
        """ Get the item type without the safety restrictions that exclude s ranks """
        first_item = self._game_config["items"]["first"]
        type_offset = self._game_config["items"]["offsets"]["type"]
        total_bytes = self._game_config["items"]["total_bytes"]
        current_item_type = self._rom_data[
            first_item + (item_idx * total_bytes) + type_offset
        ]

        return self._game_config["items"]["types"][current_item_type]
