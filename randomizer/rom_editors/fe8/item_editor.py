""" Override Module for editing items in FE8 """

from rom_editors.item_editor import ItemEditor


class FE8ItemEditor(ItemEditor):
    """ FE8 Item Editor """

    def handle_prf(self, item):
        """ Swap prf weapon for equivalent rank weapon """
        item_eq_dict = {
            self._game_config["items"]["rapier"]: 1,  # E rank sword
            self._game_config["items"]["reginleif"]: 22,  # D rank lance
            self._game_config["items"]["naglfar"]: 73,  # A rank dark
        }

        return item_eq_dict[item]
