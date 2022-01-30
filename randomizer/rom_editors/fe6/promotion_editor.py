""" Override for FE6 promotion editing """

from rom_editors.promotion_editor import PromotionEditor


class FE6PromotionEditor(PromotionEditor):
    """ Override PromotionEditor class for FE6 """

    def handle_overrides(self):
        """ Do all FE6 promotion overrides """
        self._handle_promotion_override()

    def _handle_promotion_override(self):
        """ Set the Hero Crest name and description to Master Seal """
        for override in self._game_config.items.promotional.overrides:
            # Set the pointer
            loc_bytes = self._parse_pointer(override.new_location)
            for idx, byte in enumerate(loc_bytes):
                self._rom_data[override.pointer + idx] = byte

            # Write the message
            for idx, byte in enumerate(override.bytes):
                self._rom_data[override.new_location + idx] = byte
