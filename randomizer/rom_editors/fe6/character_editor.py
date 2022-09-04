""" FE6 Override class for character editor """

from rom_editors.character_editor import CharacterEditor


class FE6CharacterEditor(CharacterEditor):
    """FE6 overrides for CharacterEditor"""

    def handle_overrides(self):
        """Perform all FE6 overrides"""
        self._handle_f_mercenary_override()
        self._handle_chad_override()
        self._handle_cath_override()
        self._handle_roy_override()

    def _handle_f_mercenary_override(self):
        """
        The Female mercenary character is almost complete. It's just
        missing a valid Name and Animation Pointer. Let's just use the
        same ones as the male mercenary
        """
        for override in self._game_config.char_stats.overrides.f_mercenary:
            self._rom_data[override.address] = override.byte

    def _handle_chad_override(self):
        """
        Chad can be any class and it's good to keep the lockpick on him
        just in case the player still has a thief class character. But
        the first chest key does not appear until the player gets to the
        shop in chapter 7. So give chad 2 5-use chest key to tide the
        player over until then.
        """
        chad = self._get_character_by_name("Chad")
        for item_pos in chad.extra_item_pos:
            self._rom_data[item_pos] = self._game_config.items.chest_key_id
            self._rom_data[item_pos + 1] = self._game_config.items.chest_key_id

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

    def _handle_roy_override(self):
        """
        The ability to let Roy sieze a chapter is based completely on
        his class and not his character. So we should zero out the bit
        on the Lord class and set the bit on Roy's new class

        Additionally, Roy's story-based promotion breaks the game when
        Roy is a different class. Adding No-Op statements in place
        didn't run the command that concludes the chapter which froze
        the game. To fix this, just copy the next 2 16-byte command strings:
        the command to fade the screen and the command to end the chapter.
        """
        # Get Roy's new class and get the address of the bit we want to set
        roy = self._get_character_by_name("Roy")
        roy_class = self._rom_data[roy.location[0]]

        first = self._game_config.class_stats.first
        offset = self._game_config.class_stats.offsets.ability2
        size = self._game_config.sizes.class_

        # Set the "Lord" bit to "false" on Roy's old class
        pos = first + (size * self._game_config.class_stats.roy) + offset
        self._rom_data[pos] &= ~self._game_config.class_stats.bit_masks.lord

        # Set the "Lord" bit to "true" on Roy's new class
        pos = first + (size * roy_class) + offset
        self._rom_data[pos] |= self._game_config.class_stats.bit_masks.lord

        # Get the position of the roy class change address, and copy the
        # next 2 commands to overwrite the current 2.
        for location in roy.story_prom_locations:
            for idx in range(32):
                self._rom_data[location + idx] = self._rom_data[location + 16 + idx]
