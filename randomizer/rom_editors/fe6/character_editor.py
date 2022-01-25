""" FE6 Override class for character editor """

from rom_editors.character_editor import CharacterEditor


class FE6CharacterEditor(CharacterEditor):
    """ FE6 overrides for CharacterEditor """

    def handle_overrides(self):
        """ Perform all FE6 overrides """
        self._handle_f_mercenary_override()

    def _handle_f_mercenary_override(self):
        """
        The Female mercenary character is almost complete. It's just
        missing a valid Name and Animation Pointer. Let's just use the
        same ones as the male mercenary
        """
        for override in self._game_config.char_stats.overrides.f_mercenary:
            self._rom_data[override.address] = override.byte
