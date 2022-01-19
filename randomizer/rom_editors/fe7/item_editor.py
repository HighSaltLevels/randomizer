""" Override Module for editing items in FE7 """

from random import randint

from rom_editors.item_editor import ItemEditor


class FE7ItemEditor(ItemEditor):
    """ FE7 Item Editor """

    def handle_overrides(self):
        """ Run all FE7 overrides """
        self._handle_prf()
        self._handle_s_rank()

    def _handle_prf(self):
        """
        Zero out item locks and set them to appropriate ranks
        """
        for item, equivalent in self._game_config["items"]["prf"].items():
            item_loc = self._get_item_loc(item)
            equivalent_loc = self._get_item_loc(equivalent)

            self._zero_out_locks(item_loc)

            rank = self._get_rank(equivalent_loc)
            self._set_rank(item_loc, rank)

    def _handle_s_rank(self):
        """ Give all bosses in final chapter s rank weapons """
        s_ranks = self._game_config["items"]["s"]
        for boss in self._game_config["classes"]["character_stats"]["final_bosses"]:
            for item_loc in self._game_config["classes"]["characters"][boss][
                "s_rank_locations"
            ]:
                item = self._rom_data[item_loc]
                item_type = self._get_item_type(item)
                rand = randint(0, len(s_ranks[item_type]) - 1)
                self._rom_data[item_loc] = s_ranks[item_type][rand]

    def _zero_out_locks(self, item_loc):
        """ Remove all item locks on the item """
        # Remove the character locks on items
        offset = self._game_config["items"]["offsets"]["ability3"]
        self._rom_data[item_loc + offset] = 0

    def _get_rank(self, item_loc):
        """ Get the rank of the item """
        offset = self._game_config["items"]["offsets"]["rank"]
        return self._rom_data[item_loc + offset]

    def _set_rank(self, item_loc, rank_value):
        """ Set rank of the item """
        offset = self._game_config["items"]["offsets"]["rank"]
        self._rom_data[item_loc + offset] = rank_value

    def _get_item_loc(self, item):
        """ Get the address of the requested {item} """
        first_item = self._game_config["items"]["first"]
        total_bytes = self._game_config["items"]["total_bytes"]

        return (item * total_bytes) + first_item
