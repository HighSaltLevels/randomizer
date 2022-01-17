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
        for mem_loc, byte in self._game_config["classes"]["character_stats"][
            "overrides"
        ]["f_mercenary"].items():
            self._rom_data[mem_loc] = byte
