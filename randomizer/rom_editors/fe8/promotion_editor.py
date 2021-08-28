""" Module for editing FE8 Promotions and Promotional Items """

from rom_editors.promotion_editor import PromotionEditor


class FE8PromotionEditor(PromotionEditor):
    """ FE8 specific promotion editor class """

    def make_all_master_seals(self):
        """ FE8 promotions need to be reconfigured too """
        super().make_all_master_seals()
        self._add_classes_to_promotion()

    def _add_classes_to_promotion(self):
        """ Add all unpromoted classes to all promotion items """
        prom_items = self._game_config["items"]["promotional"]["items"]
        classes_to_add = self._game_config["items"]["promotional"]["classes_to_add"]
        for item in prom_items:
            new_loc = prom_items[item]["new_location"]
            # Set the pointers to the new location
            for pointer in prom_items[item]["pointers"]:
                loc_bytes = self.parse_pointer(new_loc)

                for idx, _ in enumerate(loc_bytes):
                    self._rom_data[pointer + idx] = loc_bytes[idx]

            # Set classes in new location
            for idx, _ in enumerate(classes_to_add):
                self._rom_data[new_loc + idx] = classes_to_add[idx]

            # Write a zero at the ned to signal end of class list
            self._rom_data[new_loc + len(classes_to_add)] = 0

    @staticmethod
    def parse_pointer(pointer):
        """ Return the 3 bytes that make up the pointer in reversed order (little endian) """
        str_repr = str(hex(pointer)).split("x")[1]
        assert (
            len(str_repr) == 6
        ), f"New location should only be 3 bytes. Was actually {str_repr}"

        return int(str_repr[-2:], 16), int(str_repr[2:4], 16), int(str_repr[:2], 16)
