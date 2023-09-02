""" FE8 Override Class for editing items """

from rom_editors.item_editor import ItemEditor


class FE8ItemEditor(ItemEditor):
    """FE8 Item Editor Override"""

    def handle_overrides(self):
        """Perform all FE8 overrides"""
        self._handle_prf_override()

    def _handle_prf_override(self):
        """Change all prf weapon lvls to their equivalent weapon lvl"""
        for prf in self._game_config.items.prfs:
            pos = self._get_item_loc(prf.weapon)
            self._zero_out_locks(pos)
            self._rom_data[pos + self._game_config.items.offsets.level] = prf.level
