""" Override for FE6 promotion editing """

from rom_editors.promotion_editor import PromotionEditor


class FE6PromotionEditor(PromotionEditor):
    """ Override PromotionEditor class for FE6 """

    def handle_overrides(self):
        """ Do all FE6 promotion overrides """
        self._handle_promotion_override()

    def _handle_promotion_override(self):
        """ Set the Hero Crest name and description to Master Seal """
        overrides = self._game_config["items"]["promotional"]["overrides"]
        for override in {"name", "description"}:
            new_loc = overrides[override]["new_location"]
            loc_bytes = self._parse_pointer(new_loc)

            # Set the pointer
            pointer = overrides[override]["pointer"]
            for idx, byte in enumerate(loc_bytes):
                self._rom_data[pointer + idx] = byte

            # Write the message
            for idx, byte in enumerate(overrides[override]["bytes"]):
                self._rom_data[new_loc + idx] = byte
