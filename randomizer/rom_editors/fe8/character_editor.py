""" FE8 Override Class for editing characters """

from random import randint

from rom_editors.character_editor import CharacterEditor


class FE8CharacterEditor(CharacterEditor):
    """FE8 Character Editor Override"""

    def randomize_palettes(self):
        """Randomize the character palettes based on filters"""
        # Need to override the method because FE8 treats palettes differently.
        # Two 7-byte sections that we have to set for each character. One
        # section represents a color palette for all 7 potential class positions
        # in the class tree. The second section represents a class to apply that
        # palette to. So randomize each palette, and set the unpromoted and
        # promoted classes accordingly.
        for character in self._game_config.characters:
            if character.kind not in self._filters:
                for _id in character.id:
                    # First randomize all 7 palettes even if they're unused
                    pos = self._game_config.palette_stats.first_palette + (
                        self._game_config.sizes.palette * _id
                    )
                    for idx in range(self._game_config.sizes.palette):
                        rand = randint(0, self._game_config.totals.palettes - 1)
                        self._rom_data[pos + idx] = rand

                    # Set palette classes to newly randomized classes
                    # Use both promotion 1 and promotion 2. If unit does not promote,
                    # Both values also get set to 0

                    # Use the first character location to get the new class
                    new_class = self._rom_data[character.location[0]]

                    # Set base class first
                    pos = (
                        self._game_config.palette_stats.first_class
                        + (self._game_config.sizes.palette * _id)
                        + self._game_config.palette_stats.offsets.base_class
                    )
                    self._rom_data[pos] = new_class

                    # Set the 2 promotion classes
                    pos = (
                        self._game_config.palette_stats.first_class
                        + (self._game_config.sizes.palette * _id)
                        + self._game_config.palette_stats.offsets.promoted_class
                    )
                    new_prom_class = self._game_config.promotion_stats.first + (
                        self._game_config.sizes.promotion * new_class
                    )
                    for idx in range(self._game_config.totals.promotion_classes):
                        self._rom_data[pos + idx] = self._rom_data[new_prom_class + idx]
