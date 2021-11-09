""" Override Module for editing items in FE7 """

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
