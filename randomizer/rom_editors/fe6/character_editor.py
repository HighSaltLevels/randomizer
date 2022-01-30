""" FE6 Override class for character editor """

from rom_editors.character_editor import CharacterEditor


class FE6CharacterEditor(CharacterEditor):
    """ FE6 overrides for CharacterEditor """

    def handle_overrides(self):
        """ Perform all FE6 overrides """
        self._handle_f_mercenary_override()
        self._handle_cath_override()

    def _handle_f_mercenary_override(self):
        """
        The Female mercenary character is almost complete. It's just
        missing a valid Name and Animation Pointer. Let's just use the
        same ones as the male mercenary
        """
        for override in self._game_config.char_stats.overrides.f_mercenary:
            self._rom_data[override.address] = override.byte

    def _handle_cath_override(self):
        """
        Cath's behavior is to loot and the leave the chapter. If she
        is not a thief, then she can't use a lock pick and will
        immediately leave on the first turn she moves. Instead of
        changing her behavior, let's just give her a chest key and a
        door key
        """
        cath = self._get_character_by_name("Cath")
        for item_pos in cath.extra_item_pos:
            self._rom_data[item_pos] = self._game_config.items.chest_key_id
            # Use +2 to skip over the vulnerary
            self._rom_data[item_pos + 2] = self._game_config.items.door_key_id
