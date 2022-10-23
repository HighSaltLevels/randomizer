""" Module for editing promotions and promotional items """


class PromotionEditor:
    """Base PromotionEditor class"""

    def __init__(self, game_config, rom_data):
        self._game_config = game_config
        self._rom_data = rom_data

    @property
    def rom_data(self):
        """Make rom_data read only. Should only modify things one at a time"""
        return self._rom_data

    def handle_overrides(self):
        """Sub-classes can override this method to perform game-specific overrides"""

    def make_all_master_seals(self):
        """Change the appearance of all promotion items to master seals"""
        for item in self._game_config.items.promotional.items:
            self._setup_prom_item(item.location)
            self._add_classes_to_promotion(item)

        return self._rom_data

    def _add_classes_to_promotion(self, item):
        """Override the method because we need to allocate and use a different space"""
        # Set the pointers to the new location
        for pointer in item.pointers:
            loc_bytes = self._parse_pointer(item.new_location)

            for idx, _ in enumerate(loc_bytes):
                self._rom_data[pointer + idx] = loc_bytes[idx]

        # Set classes in new location
        classes_to_add = self._game_config.items.promotional.classes_to_add
        for idx, _class in enumerate(classes_to_add):
            self._rom_data[item.new_location + idx] = _class

        # Write a zero at the end to signal end of class list
        self._rom_data[item.new_location + len(classes_to_add)] = 0

    def _setup_prom_item(self, location):
        """Set the attributes for this promotional item"""
        for attr in self._game_config.items.master_seal.attributes:
            for idx, byte in enumerate(attr.bytes):
                self._rom_data[location + attr.offset + idx] = byte

    @staticmethod
    def _parse_pointer(pointer):
        """Return the 3 bytes that make up the pointer in reversed order (little endian)"""
        str_repr = str(hex(pointer)).split("x")[1]
        assert (
            len(str_repr) == 6
        ), f"New location should be exactly 3 bytes. Was actually {len(str_repr)}"
        return int(str_repr[-2:], 16), int(str_repr[2:4], 16), int(str_repr[:2], 16)
